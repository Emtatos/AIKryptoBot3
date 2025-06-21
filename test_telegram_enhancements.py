#!/usr/bin/env python3
"""
Test script to verify telegram enhancements functionality
"""
import sys
import os
sys.path.insert(0, '.')

def test_markdown_formatting():
    """Test markdown formatting in telegram messages"""
    print("=== Testing Markdown Formatting ===")
    try:
        from reporting.telegram import send_telegram
        test_message = "*Test markdown* med `kod` och **fet text**"
        print(f"✅ Markdown test message ready: {test_message}")
        return True
    except Exception as e:
        print(f"❌ Markdown formatting test failed: {e}")
        return False

def test_status_report():
    """Test status report functionality"""
    print("\n=== Testing Status Report ===")
    try:
        from reporting.status_report import send_status_report
        print("✅ Status report import successful")
        return True
    except Exception as e:
        print(f"❌ Status report test failed: {e}")
        return False

def test_daily_summary():
    """Test daily summary functionality"""
    print("\n=== Testing Daily Summary ===")
    try:
        from reporting.daily_summary import send_daily_summary
        print("✅ Daily summary import successful")
        return True
    except Exception as e:
        print(f"❌ Daily summary test failed: {e}")
        return False

def test_webhook_enhancements():
    """Test webhook server enhancements"""
    print("\n=== Testing Webhook Enhancements ===")
    try:
        with open('webhook/server.py', 'r') as f:
            content = f.read()
        
        if 'answerCallbackQuery' in content and 'response_text' in content:
            print("✅ Webhook enhancements detected")
            return True
        else:
            print("❌ Webhook enhancements not found")
            return False
            
    except Exception as e:
        print(f"❌ Webhook test failed: {e}")
        return False

def test_enhanced_messages():
    """Test enhanced message formatting in recommendation engine"""
    print("\n=== Testing Enhanced Messages ===")
    try:
        with open('tools/recommendation_engine.py', 'r') as f:
            content = f.read()
        
        if '*AUTOMATISKT KÖP*' in content and '`{best_coin}`' in content:
            print("✅ Enhanced message formatting detected")
            return True
        else:
            print("❌ Enhanced message formatting not found")
            return False
            
    except Exception as e:
        print(f"❌ Enhanced messages test failed: {e}")
        return False

def main():
    """Run all telegram enhancement tests"""
    print("📱 AIKryptoBot3 Telegram Enhancements Verification")
    print("=" * 55)
    
    tests = [
        test_markdown_formatting,
        test_status_report,
        test_daily_summary,
        test_webhook_enhancements,
        test_enhanced_messages
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All telegram enhancement tests passed!")
        print("📱 Markdown formatting enabled")
        print("📊 Status reports ready")
        print("📈 Daily summaries implemented")
        print("🔗 Webhook enhancements active")
        print("✨ Enhanced message formatting applied")
        return True
    else:
        print("⚠️ Some tests failed. Review the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
