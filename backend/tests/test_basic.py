"""
Basic tests to ensure everything works
"""

def test_import_crews():
    """Test that we can import our crews"""
    try:
        from app.crews.probate_crew import ProbateCrew
        from app.crews.divorce_crew import DivorceCrew
        print("✅ Crews imported successfully!")
        assert True
    except ImportError as e:
        print(f"❌ Failed to import crews: {e}")
        assert False, f"Failed to import crews: {e}"

def test_basic_math():
    """Basic test to ensure pytest works"""
    assert 1 + 1 == 2
    print("✅ Basic test passed!")

def test_config_import():
    """Test that config imports correctly"""
    try:
        from app.core.config import settings
        print(f"✅ Config imported! App name: {settings.APP_NAME}")
        assert True
    except ImportError as e:
        print(f"❌ Failed to import config: {e}")
        assert False

if __name__ == "__main__":
    test_import_crews()
    test_basic_math()
    test_config_import()
    print("🎉 All tests passed!")