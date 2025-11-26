#!/usr/bin/env python3
"""
TruffleHog Parser - Converts TruffleHog NDJSON results to human-readable format
Handles NDJSON (Newline Delimited JSON) format from TruffleHog scans
"""

import json
import sys
from collections import defaultdict
from datetime import datetime

def get_severity_symbol(verified):
    """Get emoji for verification status"""
    return "🔴" if verified else "🟡"

def parse_trufflehog_ndjson(file_path):
    """Parse TruffleHog NDJSON output file"""
    findings = []
    scan_info = None
    errors = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                # Skip empty lines and non-JSON lines (Docker output)
                if not line or not line.startswith('{'):
                    continue

                try:
                    data = json.loads(line)

                    # Check what type of log entry this is
                    if 'msg' in data:
                        msg = data.get('msg', '')

                        # Scan summary information
                        if msg == 'finished scanning':
                            scan_info = {
                                'chunks': data.get('chunks', 0),
                                'bytes': data.get('bytes', 0),
                                'verified_secrets': data.get('verified_secrets', 0),
                                'unverified_secrets': data.get('unverified_secrets', 0),
                                'scan_duration': data.get('scan_duration', 'unknown'),
                                'version': data.get('trufflehog_version', 'unknown')
                            }

                        # Error messages
                        elif data.get('level') == 'error':
                            errors.append({
                                'message': msg,
                                'error': data.get('error', ''),
                                'path': data.get('path', '')
                            })

                    # Secret finding
                    elif 'DetectorName' in data:
                        finding = {
                            'detector': data.get('DetectorName', 'Unknown'),
                            'verified': data.get('Verified', False),
                            'raw': data.get('Raw', ''),
                            'source': data.get('SourceName', ''),
                            'file': data.get('SourceMetadata', {}).get('Data', {}).get('Filesystem', {}).get('file', 'unknown'),
                            'line': data.get('SourceMetadata', {}).get('Data', {}).get('Filesystem', {}).get('line', 0),
                            'commit': data.get('SourceMetadata', {}).get('Data', {}).get('Git', {}).get('commit', ''),
                            'email': data.get('SourceMetadata', {}).get('Data', {}).get('Git', {}).get('email', ''),
                            'timestamp': data.get('SourceMetadata', {}).get('Data', {}).get('Git', {}).get('timestamp', ''),
                        }
                        findings.append(finding)

                except json.JSONDecodeError:
                    # Skip invalid JSON lines (Docker output, etc.)
                    continue
                except Exception as e:
                    print(f"Warning: Error parsing line {line_num}: {e}", file=sys.stderr)
                    continue

    except FileNotFoundError:
        print(f"Error: File {file_path} not found", file=sys.stderr)
        return None, None, None
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return None, None, None

    return findings, scan_info, errors

def generate_readable_report(findings, scan_info, errors, output_file):
    """Generate human-readable text report"""

    with open(output_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("=" * 80 + "\n")
        f.write("TruffleHog Secret Detection Report\n")
        f.write("=" * 80 + "\n\n")

        # TL;DR Summary
        f.write("TL;DR - Summary\n")
        f.write("=" * 80 + "\n")

        if scan_info:
            f.write(f"Scan Duration: {scan_info.get('scan_duration', 'unknown')}\n")
            f.write(f"TruffleHog Version: {scan_info.get('version', 'unknown')}\n")
            f.write(f"Chunks Scanned: {scan_info.get('chunks', 0):,}\n")
            f.write(f"Data Analyzed: {scan_info.get('bytes', 0):,} bytes ({scan_info.get('bytes', 0) / (1024*1024):.2f} MB)\n")
            f.write("\n")

            verified = scan_info.get('verified_secrets', 0)
            unverified = scan_info.get('unverified_secrets', 0)
            total = verified + unverified

            f.write(f"Total Findings: {total}\n\n")
            f.write(f"🔴 VERIFIED Secrets: {verified} (Active credentials - CRITICAL)\n")
            f.write(f"🟡 UNVERIFIED Secrets: {unverified} (Suspicious patterns - Review needed)\n")
        else:
            f.write(f"Total Findings: {len(findings)}\n")
            verified_count = sum(1 for f in findings if f['verified'])
            unverified_count = len(findings) - verified_count
            f.write(f"🔴 VERIFIED Secrets: {verified_count}\n")
            f.write(f"🟡 UNVERIFIED Secrets: {unverified_count}\n")

        f.write("\n" + "=" * 80 + "\n\n")

        # Results Interpretation
        if not findings or (scan_info and scan_info.get('verified_secrets', 0) == 0 and scan_info.get('unverified_secrets', 0) == 0):
            f.write("✅ EXCELLENT NEWS!\n")
            f.write("-" * 80 + "\n\n")
            f.write("No secrets detected in your repository!\n\n")
            f.write("What this means:\n")
            f.write("  ✓ No hardcoded credentials found\n")
            f.write("  ✓ No API keys leaked in git history\n")
            f.write("  ✓ No private keys committed to repository\n")
            f.write("  ✓ Repository is safe for public access\n")
            f.write("  ✓ Following security best practices\n\n")
        else:
            # Group findings by detector type
            by_detector = defaultdict(list)
            for finding in findings:
                by_detector[finding['detector']].append(finding)

            # Verified secrets first
            verified_findings = [f for f in findings if f['verified']]
            if verified_findings:
                f.write("🔴 CRITICAL: VERIFIED SECRETS FOUND\n")
                f.write("-" * 80 + "\n\n")
                f.write("⚠️  These are ACTIVE credentials that work!\n")
                f.write("⚠️  IMMEDIATE ACTION REQUIRED:\n")
                f.write("     1. Revoke/rotate these credentials NOW\n")
                f.write("     2. Remove from git history (use git-filter-repo)\n")
                f.write("     3. Investigate unauthorized access\n")
                f.write("     4. Update secrets management process\n\n")

                for detector, detector_findings in sorted(by_detector.items()):
                    verified = [f for f in detector_findings if f['verified']]
                    if verified:
                        f.write(f"🔴 {detector} - {len(verified)} verified secret(s)\n\n")

                        for i, finding in enumerate(verified, 1):
                            f.write(f"  Finding {i}:\n")
                            f.write(f"    Location: {finding['file']}")
                            if finding['line']:
                                f.write(f":{finding['line']}")
                            f.write("\n")

                            if finding['commit']:
                                f.write(f"    Commit: {finding['commit'][:8]}\n")
                            if finding['email']:
                                f.write(f"    Author: {finding['email']}\n")
                            if finding['timestamp']:
                                f.write(f"    Date: {finding['timestamp']}\n")

                            # Show partial secret (redacted)
                            raw = finding['raw']
                            if len(raw) > 20:
                                redacted = raw[:4] + "..." + raw[-4:]
                            else:
                                redacted = raw[:2] + "..." + (raw[-2:] if len(raw) > 4 else "")
                            f.write(f"    Secret: {redacted} (redacted)\n")
                            f.write(f"    Status: ✓ VERIFIED (works!)\n\n")

            # Unverified secrets
            unverified_findings = [f for f in findings if not f['verified']]
            if unverified_findings:
                f.write("\n🟡 UNVERIFIED SECRETS (Requires Review)\n")
                f.write("-" * 80 + "\n\n")
                f.write("These patterns look like secrets but couldn't be verified.\n")
                f.write("They might be:\n")
                f.write("  • Revoked credentials (safe)\n")
                f.write("  • Test/fake credentials (safe)\n")
                f.write("  • False positives (patterns that look like secrets)\n")
                f.write("  • Real secrets that couldn't be tested (review needed)\n\n")

                for detector, detector_findings in sorted(by_detector.items()):
                    unverified = [f for f in detector_findings if not f['verified']]
                    if unverified:
                        f.write(f"🟡 {detector} - {len(unverified)} unverified pattern(s)\n\n")

                        for i, finding in enumerate(unverified[:5], 1):  # Show first 5
                            f.write(f"  Finding {i}:\n")
                            f.write(f"    Location: {finding['file']}")
                            if finding['line']:
                                f.write(f":{finding['line']}")
                            f.write("\n")
                            f.write(f"    Status: ? Could not verify\n\n")

                        if len(unverified) > 5:
                            f.write(f"  ... and {len(unverified) - 5} more\n\n")

        # Errors section
        if errors:
            f.write("\n⚠️  Scan Warnings\n")
            f.write("-" * 80 + "\n\n")
            for error in errors[:10]:  # Show first 10 errors
                f.write(f"  • {error.get('message', 'Unknown error')}\n")
                if error.get('path'):
                    f.write(f"    Path: {error['path']}\n")
                if error.get('error'):
                    f.write(f"    Detail: {error['error'][:100]}\n")
                f.write("\n")

            if len(errors) > 10:
                f.write(f"  ... and {len(errors) - 10} more warnings\n\n")

        # Footer
        f.write("=" * 80 + "\n")
        f.write("End of TruffleHog Secret Detection Report\n")
        f.write("=" * 80 + "\n\n")

        if scan_info and scan_info.get('verified_secrets', 0) == 0:
            f.write("✅ Your repository is clean! Keep up the good security practices.\n\n")

        f.write("For full details, refer to the JSON report or pipeline logs.\n")
        f.write("TruffleHog documentation: https://github.com/trufflesecurity/trufflehog\n")

def main():
    if len(sys.argv) < 3:
        print("Usage: parse-trufflehog.py <trufflehog-report.json> <output-file.txt>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    print(f"📊 Parsing TruffleHog report: {input_file}")

    findings, scan_info, errors = parse_trufflehog_ndjson(input_file)

    if findings is None and scan_info is None:
        print("❌ Failed to parse report")
        sys.exit(1)

    print(f"   Found {len(findings)} secret finding(s)")
    if scan_info:
        print(f"   Verified: {scan_info.get('verified_secrets', 0)}")
        print(f"   Unverified: {scan_info.get('unverified_secrets', 0)}")
    if errors:
        print(f"   Warnings: {len(errors)}")

    print(f"\n📝 Generating readable report: {output_file}")
    generate_readable_report(findings, scan_info, errors, output_file)

    print(f"\n✅ Report generated successfully!")
    print(f"📄 Output: {output_file}")

if __name__ == "__main__":
    main()
