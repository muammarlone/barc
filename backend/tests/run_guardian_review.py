"""
Guardian Service Review Script
Performs forward engineering code review before git commit.
"""

import sys
import os
import io

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from agents.guardian import GuardianService
import json

def main():
    print("Guardian Service - Forward Engineering Code Review\n")
    print("="*70)

    
    # Initialize Guardian
    guardian = GuardianService(kiw_id="GUARDIAN-001")
    
    # Analyze changes
    repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    print(f"Repository Path: {repo_path}\n")
    
    changes = guardian.analyze_changes(repo_path)
    
    if not changes:
        print("✅ No uncommitted changes detected.")
        print("   All code is clean and ready for commit.\n")
        return
    
    print(f"📋 Changes Detected: {len(changes)} file(s)\n")
    for change in changes:
        print(f"   [{change.change_type}] {change.file_path} ({change.lines_changed} lines)")
    
    print("\n" + "="*70)
    print("🔍 Initiating Forward Engineering Review...\n")
    
    # Perform review
    review = guardian.forward_engineering_review(changes, repo_path)
    
    # Display results
    print("="*70)
    print("📊 GUARDIAN REVIEW RESULTS")
    print("="*70)
    print(f"Review ID:      {review.review_id}")
    print(f"Status:         {review.status}")
    print(f"Overall Grade:  {review.overall_grade}")
    print(f"Timestamp:      {review.timestamp.isoformat()}")
    print("\n" + "-"*70)
    print("SCORES:")
    print(f"  Security:        {review.security_score:.1f}/100.0")
    print(f"  Performance:     {review.performance_score:.1f}/100.0")
    print(f"  Maintainability: {review.maintainability_score:.1f}/100.0")
    print(f"  Compliance:      {review.compliance_score:.1f}/100.0")
    print("-"*70)
    
    if review.findings:
        print(f"\nFINDINGS ({len(review.findings)}):\n")
        
        # Group by severity
        critical = [f for f in review.findings if f['severity'] == 'CRITICAL']
        high = [f for f in review.findings if f['severity'] == 'HIGH']
        medium = [f for f in review.findings if f['severity'] == 'MEDIUM']
        low = [f for f in review.findings if f['severity'] == 'LOW']
        info = [f for f in review.findings if f['severity'] == 'INFO']
        
        if critical:
            print(f"[CRITICAL] ({len(critical)}):")
            for f in critical:
                print(f"   - {f['issue']}")
                print(f"     File: {f['file']}")
                print(f"     Recommendation: {f['recommendation']}\n")
        
        if high:
            print(f"[HIGH] ({len(high)}):")
            for f in high:
                print(f"   - {f['issue']}")
                print(f"     File: {f['file']}")
                print(f"     Recommendation: {f['recommendation']}\n")
        
        if medium:
            print(f"[MEDIUM] ({len(medium)}):")
            for f in medium:
                print(f"   - {f['issue']}")
                print(f"     File: {f['file']}\n")
        
        if low:
            print(f"[LOW] ({len(low)}):")
            for f in low:
                print(f"   - {f['issue']} ({f['file']})")
        
        if info:
            print(f"\n[INFO] ({len(info)}):")
            for f in info:
                print(f"   - {f['issue']} ({f['file']})")
    else:
        print("\n✅ No issues found!")
    
    print("\n" + "="*70)
    
    # Approval decision
    if guardian.approve_for_commit(review):
        print("✅ GUARDIAN APPROVAL GRANTED")
        print(f"   Approval Signature: {review.approval_signature[:32]}...")
        print("\n   Changes are approved for commit to remote main.")
        
        # Generate commit message
        commit_msg = guardian.generate_commit_message(
            review,
            "Implement V2L Parser with Tier 1 Intelligent Caching"
        )
        
        print("\n📝 Suggested Commit Message:")
        print("-"*70)
        print(commit_msg)
        print("-"*70)
        
        # Save review to file
        review_file = f"guardian_review_{review.review_id}.json"
        with open(review_file, 'w') as f:
            json.dump(review.dict(), f, indent=2, default=str)
        print(f"\n💾 Review saved to: {review_file}")
        
        return 0
    else:
        print("❌ GUARDIAN APPROVAL DENIED")
        print(f"   Status: {review.status}")
        print(f"\n   Remediation Required:")
        for req in review.remediation_required:
            print(f"   • {req}")
        
        print("\n   Please address the issues above before committing.")
        return 1

if __name__ == "__main__":
    exit(main())
