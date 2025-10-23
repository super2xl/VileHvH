#!/usr/bin/env python3
"""
Quick test script to verify system detection is working
Run this before the full setup to check if your system is detected correctly
"""

from system_detect import detect_system, check_package_installed

def main():
    print("Testing system detection...\n")
    
    # Detect system
    sys_info = detect_system()
    
    print("\n" + "="*60)
    print("System Detection Test Results")
    print("="*60)
    
    # Check for common packages
    print("\nChecking for common packages:")
    
    test_packages = []
    
    # Add test packages based on detected package managers
    for pm in sys_info.package_managers:
        if pm.value in ["pacman", "yay", "paru"]:
            test_packages = ["python", "git", "base-devel"]
            break
        elif pm.value == "apt":
            test_packages = ["python3", "git", "dpkg"]
            break
        elif pm.value == "winget":
            test_packages = ["Python.Python.3", "Git.Git"]
            break
    
    for package in test_packages:
        installed = check_package_installed(package, sys_info)
        status = "✓ INSTALLED" if installed else "✗ NOT FOUND"
        print(f"  {package:<20} {status}")
    
    print("\n" + "="*60)
    print("System detection test complete!")
    print("="*60)
    
    if sys_info.os_type.value in ["linux", "windows"]:
        print("\n✓ Your system is supported!")
        print("  You can proceed with running setup.py")
    else:
        print("\n✗ Your system may not be fully supported")
        print("  You may encounter issues running setup.py")

if __name__ == "__main__":
    main()

