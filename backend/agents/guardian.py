import logging
import hashlib
import subprocess
import os
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
from pydantic import BaseModel

logger = logging.getLogger("Guardian-Service")

class CodeChange(BaseModel):
    file_path: str
    change_type: str  # "ADDED", "MODIFIED", "DELETED"
    lines_changed: int
    diff_hash: str
    author: str = "Antigravity-AI"
    timestamp: datetime = datetime.utcnow()

class GuardianReview(BaseModel):
    review_id: str
    status: str  # "APPROVED", "REJECTED", "REQUIRES_REMEDIATION"
    findings: List[Dict[str, Any]]
    security_score: float  # 0.0 - 100.0
    performance_score: float
    maintainability_score: float
    compliance_score: float
    overall_grade: str  # "A+", "A", "B", "C", "D", "F"
    remediation_required: List[str]
    approval_signature: str  # SHA-256 hash of the review
    timestamp: datetime = datetime.utcnow()

class GuardianService:
    """
    Forward Engineering Quality Assurance Agent.
    Performs comprehensive code review before git commits.
    """
    
    def __init__(self, kiw_id: str = "GUARDIAN-001"):
        self.kiw_id = kiw_id
        self.review_history: List[GuardianReview] = []
        
    def analyze_changes(self, repo_path: str) -> List[CodeChange]:
        """
        Step 1: Detect all uncommitted changes in the repository.
        """
        logger.info("Guardian: Analyzing uncommitted changes...")
        
        try:
            # Get git status
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            changes = []
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                    
                status = line[:2].strip()
                file_path = line[3:].strip()
                
                # Determine change type
                if status == 'M':
                    change_type = "MODIFIED"
                elif status == 'A' or status == '??':
                    change_type = "ADDED"
                elif status == 'D':
                    change_type = "DELETED"
                else:
                    change_type = "UNKNOWN"
                
                # Get diff hash
                try:
                    diff_result = subprocess.run(
                        ["git", "diff", "HEAD", file_path],
                        cwd=repo_path,
                        capture_output=True,
                        text=True
                    )
                    diff_hash = hashlib.sha256(diff_result.stdout.encode()).hexdigest()
                    lines_changed = len(diff_result.stdout.split('\n'))
                except:
                    diff_hash = "N/A"
                    lines_changed = 0
                
                changes.append(CodeChange(
                    file_path=file_path,
                    change_type=change_type,
                    lines_changed=lines_changed,
                    diff_hash=diff_hash[:16]
                ))
            
            logger.info(f"Guardian: Found {len(changes)} file(s) with changes")
            return changes
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Guardian: Failed to analyze changes: {e}")
            return []
    
    def forward_engineering_review(self, changes: List[CodeChange], repo_path: str) -> GuardianReview:
        """
        Step 2: Perform forward engineering analysis.
        Evaluates code for future-proofing, scalability, and architectural integrity.
        """
        logger.info("Guardian: Initiating Forward Engineering Review...")
        
        findings = []
        
        # 1. Security Audit
        security_findings = self._audit_security(changes, repo_path)
        findings.extend(security_findings)
        
        # 2. Performance Analysis
        performance_findings = self._analyze_performance(changes, repo_path)
        findings.extend(performance_findings)
        
        # 3. Maintainability Check
        maintainability_findings = self._check_maintainability(changes, repo_path)
        findings.extend(maintainability_findings)
        
        # 4. Compliance Verification
        compliance_findings = self._verify_compliance(changes, repo_path)
        findings.extend(compliance_findings)
        
        # Calculate scores
        security_score = self._calculate_security_score(security_findings)
        performance_score = self._calculate_performance_score(performance_findings)
        maintainability_score = self._calculate_maintainability_score(maintainability_findings)
        compliance_score = self._calculate_compliance_score(compliance_findings)
        
        # Determine overall grade
        avg_score = (security_score + performance_score + maintainability_score + compliance_score) / 4
        overall_grade = self._score_to_grade(avg_score)
        
        # Determine status
        critical_issues = [f for f in findings if f.get("severity") == "CRITICAL"]
        if critical_issues:
            status = "REJECTED"
        elif avg_score < 70.0:
            status = "REQUIRES_REMEDIATION"
        else:
            status = "APPROVED"
        
        # Generate approval signature
        review_data = {
            "findings": findings,
            "scores": {
                "security": security_score,
                "performance": performance_score,
                "maintainability": maintainability_score,
                "compliance": compliance_score
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        approval_signature = hashlib.sha256(str(review_data).encode()).hexdigest()
        
        review = GuardianReview(
            review_id=f"GR-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
            status=status,
            findings=findings,
            security_score=security_score,
            performance_score=performance_score,
            maintainability_score=maintainability_score,
            compliance_score=compliance_score,
            overall_grade=overall_grade,
            remediation_required=[f["issue"] for f in findings if f.get("severity") in ["CRITICAL", "HIGH"]],
            approval_signature=approval_signature
        )
        
        self.review_history.append(review)
        return review
    
    def _audit_security(self, changes: List[CodeChange], repo_path: str) -> List[Dict[str, Any]]:
        """
        Security audit based on AI Security Gold Standard (5-Layer Defense).
        """
        findings = []
        
        for change in changes:
            if not change.file_path.endswith('.py'):
                continue
                
            full_path = os.path.join(repo_path, change.file_path)
            if not os.path.exists(full_path):
                continue
            
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for hardcoded secrets
                if self._contains_secrets(content):
                    findings.append({
                        "file": change.file_path,
                        "severity": "CRITICAL",
                        "category": "SECURITY",
                        "issue": "Potential hardcoded secrets detected",
                        "recommendation": "Use KIWVault or environment variables for secret management"
                    })
                
                # Check for SQL injection vulnerabilities
                if self._has_sql_injection_risk(content):
                    findings.append({
                        "file": change.file_path,
                        "severity": "CRITICAL",
                        "category": "SECURITY",
                        "issue": "Potential SQL injection vulnerability",
                        "recommendation": "Use parameterized queries or ORM"
                    })
                
                # Check for missing input validation
                if self._missing_input_validation(content):
                    findings.append({
                        "file": change.file_path,
                        "severity": "HIGH",
                        "category": "SECURITY",
                        "issue": "Missing input validation on API endpoints",
                        "recommendation": "Implement Pydantic validation for all inputs"
                    })
                    
            except Exception as e:
                logger.warning(f"Guardian: Could not read {change.file_path}: {e}")
        
        return findings
    
    def _analyze_performance(self, changes: List[CodeChange], repo_path: str) -> List[Dict[str, Any]]:
        """
        Performance analysis for compute optimization and scalability.
        """
        findings = []
        
        for change in changes:
            if not change.file_path.endswith('.py'):
                continue
                
            full_path = os.path.join(repo_path, change.file_path)
            if not os.path.exists(full_path):
                continue
            
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for missing caching opportunities
                if 'def ' in content and '@lru_cache' not in content and 'cache' in change.file_path.lower():
                    findings.append({
                        "file": change.file_path,
                        "severity": "INFO",
                        "category": "PERFORMANCE",
                        "issue": "Caching implementation detected - verify LRU eviction logic",
                        "recommendation": "Ensure cache size limits and eviction policies are properly configured"
                    })
                
                # Check for synchronous blocking operations
                if 'requests.get' in content or 'requests.post' in content:
                    if 'async def' not in content:
                        findings.append({
                            "file": change.file_path,
                            "severity": "LOW",
                            "category": "PERFORMANCE",
                            "issue": "Synchronous HTTP requests detected",
                            "recommendation": "Consider using async HTTP client (httpx) for better concurrency"
                        })
                        
            except Exception as e:
                logger.warning(f"Guardian: Could not read {change.file_path}: {e}")
        
        return findings
    
    def _check_maintainability(self, changes: List[CodeChange], repo_path: str) -> List[Dict[str, Any]]:
        """
        Maintainability check for code quality and documentation.
        """
        findings = []
        
        for change in changes:
            if not change.file_path.endswith('.py'):
                continue
                
            full_path = os.path.join(repo_path, change.file_path)
            if not os.path.exists(full_path):
                continue
            
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for docstrings
                if 'class ' in content or 'def ' in content:
                    if '"""' not in content and "'''" not in content:
                        findings.append({
                            "file": change.file_path,
                            "severity": "LOW",
                            "category": "MAINTAINABILITY",
                            "issue": "Missing docstrings",
                            "recommendation": "Add comprehensive docstrings for classes and functions"
                        })
                
                # Check for logging
                if 'logger' not in content and change.file_path.startswith('backend/agents'):
                    findings.append({
                        "file": change.file_path,
                        "severity": "MEDIUM",
                        "category": "MAINTAINABILITY",
                        "issue": "Missing logging statements",
                        "recommendation": "Add logger for debugging and audit trails"
                    })
                        
            except Exception as e:
                logger.warning(f"Guardian: Could not read {change.file_path}: {e}")
        
        return findings
    
    def _verify_compliance(self, changes: List[CodeChange], repo_path: str) -> List[Dict[str, Any]]:
        """
        Compliance verification against KIW standards and regulatory requirements.
        """
        findings = []
        
        for change in changes:
            if not change.file_path.endswith('.py'):
                continue
                
            full_path = os.path.join(repo_path, change.file_path)
            if not os.path.exists(full_path):
                continue
            
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for type hints
                if 'def ' in content:
                    if '->' not in content:
                        findings.append({
                            "file": change.file_path,
                            "severity": "LOW",
                            "category": "COMPLIANCE",
                            "issue": "Missing type hints",
                            "recommendation": "Add type hints for better code quality and IDE support"
                        })
                
                # Check for Pydantic models
                if 'BaseModel' in content:
                    findings.append({
                        "file": change.file_path,
                        "severity": "INFO",
                        "category": "COMPLIANCE",
                        "issue": "Pydantic models detected - KIW compliant",
                        "recommendation": "Ensure all fields have proper validation"
                    })
                        
            except Exception as e:
                logger.warning(f"Guardian: Could not read {change.file_path}: {e}")
        
        return findings
    
    def _contains_secrets(self, content: str) -> bool:
        """Check for potential hardcoded secrets."""
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']'
        ]
        for pattern in secret_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False
    
    def _has_sql_injection_risk(self, content: str) -> bool:
        """Check for SQL injection vulnerabilities."""
        # Look for string concatenation in SQL queries
        if 'execute(' in content and '+' in content:
            return True
        if 'execute(' in content and 'f"' in content:
            return True
        return False
    
    def _missing_input_validation(self, content: str) -> bool:
        """Check for missing input validation."""
        # If there's a FastAPI endpoint without Pydantic validation
        if '@app.post' in content or '@app.get' in content:
            if 'BaseModel' not in content:
                return True
        return False
    
    def _calculate_security_score(self, findings: List[Dict]) -> float:
        """Calculate security score (0-100)."""
        security_findings = [f for f in findings if f.get("category") == "SECURITY"]
        critical = len([f for f in security_findings if f.get("severity") == "CRITICAL"])
        high = len([f for f in security_findings if f.get("severity") == "HIGH"])
        
        if critical > 0:
            return max(0.0, 50.0 - (critical * 25))
        elif high > 0:
            return max(70.0, 100.0 - (high * 10))
        else:
            return 100.0
    
    def _calculate_performance_score(self, findings: List[Dict]) -> float:
        """Calculate performance score (0-100)."""
        perf_findings = [f for f in findings if f.get("category") == "PERFORMANCE"]
        medium = len([f for f in perf_findings if f.get("severity") == "MEDIUM"])
        low = len([f for f in perf_findings if f.get("severity") == "LOW"])
        return max(70.0, 100.0 - (medium * 5) - (low * 2))
    
    def _calculate_maintainability_score(self, findings: List[Dict]) -> float:
        """Calculate maintainability score (0-100)."""
        maint_findings = [f for f in findings if f.get("category") == "MAINTAINABILITY"]
        medium = len([f for f in maint_findings if f.get("severity") == "MEDIUM"])
        low = len([f for f in maint_findings if f.get("severity") == "LOW"])
        return max(70.0, 100.0 - (medium * 5) - (low * 2))
    
    def _calculate_compliance_score(self, findings: List[Dict]) -> float:
        """Calculate compliance score (0-100)."""
        comp_findings = [f for f in findings if f.get("category") == "COMPLIANCE"]
        high = len([f for f in comp_findings if f.get("severity") == "HIGH"])
        medium = len([f for f in comp_findings if f.get("severity") == "MEDIUM"])
        low = len([f for f in comp_findings if f.get("severity") == "LOW"])
        return max(70.0, 100.0 - (high * 15) - (medium * 5) - (low * 1))
    
    def _score_to_grade(self, score: float) -> str:
        """Convert numeric score to letter grade."""
        if score >= 95: return "A+"
        elif score >= 90: return "A"
        elif score >= 80: return "B"
        elif score >= 70: return "C"
        elif score >= 60: return "D"
        else: return "F"
    
    def approve_for_commit(self, review: GuardianReview) -> bool:
        """
        Step 3: Determine if changes are approved for commit.
        """
        if review.status == "APPROVED":
            logger.info(f"✅ Guardian APPROVED commit: {review.review_id} (Grade: {review.overall_grade})")
            return True
        else:
            logger.warning(f"❌ Guardian REJECTED commit: {review.review_id} (Status: {review.status})")
            logger.warning(f"   Remediation required: {review.remediation_required}")
            return False
    
    def generate_commit_message(self, review: GuardianReview, base_message: str) -> str:
        """
        Generate Guardian-approved commit message.
        """
        commit_msg = f"[GUARDIAN-{review.status}] {base_message}\n\n"
        commit_msg += f"Guardian Review: {review.review_id}\n"
        commit_msg += f"Overall Grade: {review.overall_grade}\n"
        commit_msg += f"Security: {review.security_score:.1f} | "
        commit_msg += f"Performance: {review.performance_score:.1f} | "
        commit_msg += f"Maintainability: {review.maintainability_score:.1f} | "
        commit_msg += f"Compliance: {review.compliance_score:.1f}\n"
        commit_msg += f"Approval Signature: {review.approval_signature[:16]}...\n"
        
        if review.findings:
            commit_msg += f"\nFindings ({len(review.findings)}):\n"
            for finding in review.findings[:5]:  # Limit to first 5
                commit_msg += f"- [{finding['severity']}] {finding['issue']} ({finding['file']})\n"
        
        return commit_msg
