import hashlib
import json
import logging
from typing import Dict, List, Any, Optional
from functools import lru_cache
from schemas.gados import GADOSGraph, GADOSNode, GADOSEdge, GADOSMetadata

logger = logging.getLogger("V2L-Parser")

class V2LParser:
    """
    Vision-to-Logic Parser with Tier 1 Intelligent Caching.
    Implements SHA-256 fingerprint cache and compliance result cache.
    """
    def __init__(self, kiw_id: str, cache_size: int = 128):
        self.kiw_id = kiw_id
        self._fingerprint_cache: Dict[str, str] = {}  # {input_hash: graph_fingerprint}
        self._compliance_cache: Dict[str, Dict[str, Any]] = {}  # {cache_key: verification_result}
        self._cache_size = cache_size
        self._cache_hits = 0
        self._cache_misses = 0

    def decompose(self, raw_input: Dict[str, Any]) -> List[Dict]:
        """
        Step 1: Extract visual primitives from raw input.
        """
        return raw_input.get("primitives", [])
    
    def _generate_input_hash(self, primitives: List[Dict]) -> str:
        """
        Generate a deterministic hash of the input primitives for cache lookup.
        """
        canonical_input = json.dumps(primitives, sort_keys=True)
        return hashlib.sha256(canonical_input.encode()).hexdigest()

    def explore(self, primitives: List[Dict]) -> GADOSGraph:
        """
        Step 2: Build GADOS graph from primitives with intelligent caching.
        """
        # Generate input hash for cache lookup
        input_hash = self._generate_input_hash(primitives)
        
        # Check fingerprint cache
        if input_hash in self._fingerprint_cache:
            cached_fingerprint = self._fingerprint_cache[input_hash]
            self._cache_hits += 1
            logger.info(f"Fingerprint Cache HIT ({self._cache_hits} hits, {self._cache_misses} misses): {input_hash[:8]}...")
            # Still need to build the graph, but we can skip expensive fingerprinting
            nodes, edges = self._build_graph_components(primitives)
            metadata = GADOSMetadata(kiw_id=self.kiw_id, fingerprint=cached_fingerprint)
            return GADOSGraph(nodes=nodes, edges=edges, metadata=metadata)
        
        # Cache miss - build graph and compute fingerprint
        self._cache_misses += 1
        logger.info(f"Fingerprint Cache MISS ({self._cache_hits} hits, {self._cache_misses} misses): {input_hash[:8]}...")
        
        nodes, edges = self._build_graph_components(primitives)
        fingerprint = self._generate_fingerprint(nodes, edges)
        
        # Store in cache with LRU eviction
        self._fingerprint_cache[input_hash] = fingerprint
        self._evict_cache_if_needed()
        
        metadata = GADOSMetadata(kiw_id=self.kiw_id, fingerprint=fingerprint)
        return GADOSGraph(nodes=nodes, edges=edges, metadata=metadata)
    
    def _build_graph_components(self, primitives: List[Dict]) -> tuple:
        """
        Helper method to build nodes and edges from primitives.
        """
        nodes = []
        edges = []
        for p in primitives:
            if p["type"] == "node":
                nodes.append(GADOSNode(
                    type=p["category"],
                    label=p["name"],
                    properties=p.get("props", {}),
                    coordinates=p.get("coords")
                ))
            elif p["type"] == "edge":
                edges.append(GADOSEdge(
                    source=p["from"],
                    target=p["to"],
                    type=p["protocol"],
                    weight=p.get("weight")
                ))
        return nodes, edges
    
    def _evict_cache_if_needed(self):
        """
        LRU eviction: Remove oldest entries if cache exceeds size limit.
        """
        if len(self._fingerprint_cache) > self._cache_size:
            # Remove oldest entry (first key in dict)
            oldest_key = next(iter(self._fingerprint_cache))
            del self._fingerprint_cache[oldest_key]
            logger.debug(f"Cache evicted: {oldest_key[:8]}...")
        
        if len(self._compliance_cache) > self._cache_size:
            oldest_key = next(iter(self._compliance_cache))
            del self._compliance_cache[oldest_key]
            logger.debug(f"Compliance cache evicted: {oldest_key[:16]}...")

    def _generate_fingerprint(self, nodes: List[GADOSNode], edges: List[GADOSEdge]) -> str:
        """
        Generates a deterministic SHA-256 WL-style hash for the graph.
        """
        # Sort for determinism
        node_data = sorted([n.model_dump_json() for n in nodes])
        edge_data = sorted([e.model_dump_json() for e in edges])
        combined = "".join(node_data + edge_data)
        return hashlib.sha256(combined.encode()).hexdigest()

    def synthesize(self, graph: GADOSGraph) -> Dict[str, Any]:
        """
        Step 3: Formalize into auditable output.
        """
        return graph.model_dump()

    def critique(self, graph: GADOSGraph) -> List[str]:
        issues = []
        node_ids = {n.id for n in graph.nodes}
        for edge in graph.edges:
            if edge.source not in node_ids or edge.target not in node_ids:
                issues.append(f"Dangling edge detected: {edge.source} -> {edge.target}")
        return issues

    def verify(self, graph: GADOSGraph, standards: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 5: Verify graph against standards with compliance result caching.
        """
        # Generate cache key from graph fingerprint and standards version
        standards_version = standards.get("version", "1.0")
        cache_key = f"{graph.metadata.fingerprint}:{standards_version}"
        
        # Check compliance cache
        if cache_key in self._compliance_cache:
            logger.info(f"Compliance Cache HIT: {cache_key[:16]}...")
            return self._compliance_cache[cache_key]
        
        logger.info(f"Compliance Cache MISS: {cache_key[:16]}...")
        
        # Run verification
        results = []
        overall_status = "CERTIFIED"
        circuit_count = len([e for e in graph.edges if e.type in ["WebRTC", "SIP", "Direct"]])
        if circuit_count < 2:
            results.append({
                "req_id": "NW-REQ-01",
                "status": "FAIL",
                "finding": f"Only {circuit_count} circuits detected. Minimum of 2 required.",
                "evidence": [e.id for e in graph.edges]
            })
            overall_status = "NON-COMPLIANT"
        else:
            results.append({"req_id": "NW-REQ-01", "status": "PASS", "finding": f"{circuit_count} circuits validated."})

        for edge in graph.edges:
            if edge.weight and "latency_ms" in edge.weight:
                latency = edge.weight["latency_ms"]
                if latency > 150.0:
                    results.append({
                        "req_id": "NW-REQ-02",
                        "status": "FAIL",
                        "finding": f"Latency of {latency}ms exceeds 150ms threshold.",
                        "edge_id": edge.id
                    })
                    overall_status = "NON-COMPLIANT"
        
        verification_result = {
            "status": overall_status,
            "kiw_id": self.kiw_id,
            "findings": results,
            "logic_trace": "V2L-PIPELINE-COMPLETE",
            "fingerprint": graph.metadata.fingerprint
        }
        
        # Store in compliance cache
        self._compliance_cache[cache_key] = verification_result
        self._evict_cache_if_needed()
        
        return verification_result
    
    def invalidate_cache(self, reason: str = "Manual invalidation"):
        """
        Clear all caches and log the invalidation for audit trails.
        """
        logger.warning(f"Cache invalidated: {reason}")
        self._fingerprint_cache.clear()
        self._compliance_cache.clear()
        self._cache_hits = 0
        self._cache_misses = 0
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Return cache performance metrics.
        """
        total_requests = self._cache_hits + self._cache_misses
        hit_rate = (self._cache_hits / total_requests * 100) if total_requests > 0 else 0.0
        
        return {
            "cache_hits": self._cache_hits,
            "cache_misses": self._cache_misses,
            "hit_rate_percent": round(hit_rate, 2),
            "fingerprint_cache_size": len(self._fingerprint_cache),
            "compliance_cache_size": len(self._compliance_cache),
            "max_cache_size": self._cache_size
        }
