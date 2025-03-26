#!/usr/bin/env python3
"""
Test runner script for the Liquor Management System.
This script can run all tests or specific test categories.
"""

import os
import sys
import argparse
import subprocess
import time
from datetime import datetime

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Define test categories
TEST_CATEGORIES = {
    'unit': [
        'auth_service',
        'core_service',
        'inventory_service',
        'purchase_service',
        'sales_service',
        'accounting_service',
        'reporting_service'
    ],
    'integration': [
        'auth_inventory',
        'auth_core',
        'inventory_sales',
        'sales_accounting',
        'purchase_inventory',
        'inventory_reporting'
    ],
    'e2e': [
        'sales_flow',
        'inventory_flow',
        'purchase_flow',
        'accounting_flow',
        'reporting_flow'
    ],
    'performance': [
        'api_load',
        'database_load',
        'kafka_throughput'
    ],
    'security': [
        'auth_security',
        'api_security',
        'data_security'
    ]
}

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Run tests for the Liquor Management System')
    
    parser.add_argument(
        '--category',
        choices=['all', 'unit', 'integration', 'e2e', 'performance', 'security'],
        default='all',
        help='Test category to run (default: all)'
    )
    
    parser.add_argument(
        '--service',
        choices=[
            'all', 'auth', 'core', 'inventory', 'purchase', 
            'sales', 'accounting', 'reporting'
        ],
        default='all',
        help='Service to test (default: all)'
    )
    
    parser.add_argument(
        '--module',
        help='Specific test module to run (e.g., auth_inventory, sales_flow)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--junit-xml',
        action='store_true',
        help='Generate JUnit XML reports'
    )
    
    parser.add_argument(
        '--coverage',
        action='store_true',
        help='Generate coverage reports'
    )
    
    return parser.parse_args()

def get_test_paths(category, service, module):
    """Get the test paths based on the category, service, and module."""
    base_path = os.path.join('src')
    paths = []
    
    if module:
        # If a specific module is specified, find its path
        if category == 'unit':
            for svc in TEST_CATEGORIES['unit']:
                if module in svc:
                    paths.append(os.path.join(base_path, svc))
                    break
        else:
            paths.append(os.path.join(base_path, f'{category}_tests', module))
    elif category != 'all' and service != 'all':
        # If both category and service are specified
        if category == 'unit':
            for svc in TEST_CATEGORIES['unit']:
                if service in svc:
                    paths.append(os.path.join(base_path, svc))
        else:
            for mod in TEST_CATEGORIES[category]:
                if service in mod:
                    paths.append(os.path.join(base_path, f'{category}_tests', mod))
    elif category != 'all':
        # If only category is specified
        if category == 'unit':
            for svc in TEST_CATEGORIES['unit']:
                paths.append(os.path.join(base_path, svc))
        else:
            for mod in TEST_CATEGORIES[category]:
                paths.append(os.path.join(base_path, f'{category}_tests', mod))
    elif service != 'all':
        # If only service is specified
        for cat in TEST_CATEGORIES:
            if cat == 'unit':
                for svc in TEST_CATEGORIES[cat]:
                    if service in svc:
                        paths.append(os.path.join(base_path, svc))
            else:
                for mod in TEST_CATEGORIES[cat]:
                    if service in mod:
                        paths.append(os.path.join(base_path, f'{cat}_tests', mod))
    else:
        # If neither category nor service is specified, run all tests
        for cat in TEST_CATEGORIES:
            if cat == 'unit':
                for svc in TEST_CATEGORIES[cat]:
                    paths.append(os.path.join(base_path, svc))
            else:
                for mod in TEST_CATEGORIES[cat]:
                    paths.append(os.path.join(base_path, f'{cat}_tests', mod))
    
    return paths

def run_tests(paths, verbose, junit_xml, coverage):
    """Run the tests for the specified paths."""
    results = {}
    start_time = time.time()
    
    for path in paths:
        print(f"\n{'='*80}")
        print(f"Running tests in: {path}")
        print(f"{'='*80}")
        
        # Build the pytest command
        cmd = ['python', '-m', 'pytest']
        
        if verbose:
            cmd.append('-v')
        
        if junit_xml:
            report_dir = os.path.join('test_reports', path.replace('/', '_'))
            os.makedirs(report_dir, exist_ok=True)
            cmd.extend(['--junitxml', os.path.join(report_dir, 'results.xml')])
        
        if coverage:
            cmd.extend(['--cov', path, '--cov-report', 'term', '--cov-report', 'html:coverage_reports'])
        
        cmd.append(path)
        
        # Run the tests
        try:
            result = subprocess.run(cmd, check=False)
            results[path] = result.returncode == 0
        except Exception as e:
            print(f"Error running tests in {path}: {e}")
            results[path] = False
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Print summary
    print(f"\n{'='*80}")
    print(f"Test Summary ({duration:.2f} seconds)")
    print(f"{'='*80}")
    
    passed = sum(1 for success in results.values() if success)
    failed = len(results) - passed
    
    for path, success in results.items():
        status = "PASSED" if success else "FAILED"
        print(f"{path}: {status}")
    
    print(f"\nTotal: {len(results)}, Passed: {passed}, Failed: {failed}")
    
    return all(results.values())

def main():
    """Main function."""
    args = parse_args()
    
    print(f"\n{'='*80}")
    print(f"Liquor Management System Test Runner")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}")
    
    paths = get_test_paths(args.category, args.service, args.module)
    
    if not paths:
        print("No test paths found for the specified criteria.")
        return 1
    
    print(f"Test paths: {', '.join(paths)}")
    
    success = run_tests(paths, args.verbose, args.junit_xml, args.coverage)
    
    print(f"\n{'='*80}")
    print(f"Test run completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Overall status: {'PASSED' if success else 'FAILED'}")
    print(f"{'='*80}")
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
