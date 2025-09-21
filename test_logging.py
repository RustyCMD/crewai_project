#!/usr/bin/env python3
"""
Test script to verify logging configuration and identify issues
"""

import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv
from logging_config import setup_logging, get_logger, log_safe

# Load environment variables
load_dotenv()

def test_basic_logging():
    """Test basic logging functionality"""
    print("=" * 60)
    print("[SEARCH] TESTING BASIC LOGGING FUNCTIONALITY")
    print("=" * 60)

    # Test 1: Basic logging setup
    print("\n1. Testing basic logging setup...")

    log_level = os.getenv('LOG_LEVEL', 'INFO')
    log_file = os.getenv('LOG_FILE', './logs/crewai_game_dev.log')

    print(f"   LOG_LEVEL from env: {log_level}")
    print(f"   LOG_FILE from env: {log_file}")

    # Test 2: Configure logging using new system
    print("\n2. Configuring logging with new system...")

    try:
        setup_logging()
        print("   [OK] New logging configuration successful")
    except Exception as e:
        print(f"   [ERROR] New logging configuration failed: {e}")
        return False

    # Test 3: Create logger and test messages
    print("\n3. Testing log messages with safe logging...")

    logger = get_logger(__name__)

    # Test different log levels with safe logging
    log_safe(logger, "debug", "[BUG] This is a DEBUG message")
    log_safe(logger, "info", "[INFO] This is an INFO message")
    log_safe(logger, "warning", "[WARNING] This is a WARNING message")
    log_safe(logger, "error", "[ERROR] This is an ERROR message")
    log_safe(logger, "critical", "[ALERT] This is a CRITICAL message")

    print("   [OK] Safe log messages sent")

    # Test 4: Test problematic Unicode characters
    print("\n4. Testing Unicode character handling...")

    # These should now work without errors
    logger.info("Testing emoji: 🎮 🚀 ✅ ❌ ⚠️")
    logger.info("Testing arrows: → ← ↑ ↓")
    logger.info("Testing special chars: 📊 💬 🔒 🔗")

    print("   [OK] Unicode test messages sent")
    
    # Test 5: Check if log file was created and has content
    print("\n5. Checking log file...")

    if os.path.exists(log_file):
        file_size = os.path.getsize(log_file)
        print(f"   [OK] Log file exists: {log_file}")
        print(f"   [CHART] Log file size: {file_size} bytes")

        if file_size > 0:
            print("   [OK] Log file has content")

            # Read and display last few lines
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    print(f"   [FILE] Total lines in log file: {len(lines)}")

                    if lines:
                        print("   [NOTE] Last few log entries:")
                        for line in lines[-5:]:  # Show last 5 lines
                            print(f"      {line.strip()}")
                    else:
                        print("   [WARNING] Log file is empty")
            except Exception as e:
                print(f"   [ERROR] Error reading log file: {e}")
        else:
            print("   [WARNING] Log file is empty")
    else:
        print(f"   [ERROR] Log file does not exist: {log_file}")
        return False

    return True

def test_collaborative_logging():
    """Test collaborative development logging"""
    print("\n" + "=" * 60)
    print("🔍 TESTING COLLABORATIVE LOGGING")
    print("=" * 60)
    
    # Test collaborative_development.log
    collab_log = "collaborative_development.log"
    
    print(f"\n1. Checking collaborative log file: {collab_log}")
    
    if os.path.exists(collab_log):
        file_size = os.path.getsize(collab_log)
        print(f"   ✅ Collaborative log file exists")
        print(f"   📊 File size: {file_size} bytes")
        
        if file_size > 0:
            try:
                with open(collab_log, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.strip().split('\n') if content.strip() else []
                    print(f"   📄 Lines in file: {len(lines)}")
                    
                    if lines and lines[0]:  # Check if there's actual content
                        print("   📝 Recent entries:")
                        for line in lines[-3:]:  # Show last 3 lines
                            if line.strip():
                                print(f"      {line}")
                    else:
                        print("   ⚠️  File exists but is empty or contains only whitespace")
            except Exception as e:
                print(f"   ❌ Error reading collaborative log: {e}")
        else:
            print("   ⚠️  Collaborative log file is empty")
    else:
        print(f"   ❌ Collaborative log file does not exist: {collab_log}")
    
    # Test agent communication logging
    print("\n2. Testing agent communication logging...")
    
    try:
        from agent_communication import comm_hub
        
        # Test sending a message (this should generate log entries)
        comm_hub.send_message("TestAgent1", "TestAgent2", "Test logging message")
        comm_hub.update_status("TestAgent1", "Testing logging functionality")
        
        print("   ✅ Agent communication test messages sent")
        
        # Check if the communication file exists
        comm_file = comm_hub.communication_file
        if os.path.exists(comm_file):
            print(f"   ✅ Communication file exists: {comm_file}")
        else:
            print(f"   ❌ Communication file missing: {comm_file}")
            
    except Exception as e:
        print(f"   ❌ Error testing agent communication: {e}")

def main():
    """Main test function"""
    print("🧪 LOGGING SYSTEM DIAGNOSTIC TEST")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test basic logging
    basic_success = test_basic_logging()
    
    # Test collaborative logging
    test_collaborative_logging()
    
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    if basic_success:
        print("✅ Basic logging functionality: WORKING")
    else:
        print("❌ Basic logging functionality: FAILED")
    
    print("\n💡 RECOMMENDATIONS:")
    print("1. Check if log files are being created in the correct directories")
    print("2. Verify file permissions for log directories")
    print("3. Ensure logging configuration is not being overridden")
    print("4. Check if multiple logging.basicConfig() calls are conflicting")
    
    print(f"\n⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
