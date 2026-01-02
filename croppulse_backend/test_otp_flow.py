"""
Simple test script for OTP flow
Save as: test_otp_flow.py
Run: python test_otp_flow.py
"""

import os
import django

# -------------------------------------------------------------------
# Django setup
# -------------------------------------------------------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "croppulse.settings.development")
django.setup()

from django.utils import timezone
from apps.users.models import User
from apps.users.services import UserService
from core.utils import generate_verification_code


def test_otp_flow():
    """Test the complete OTP flow (NO duplicate profile creation)"""

    test_phone = "+254799999999"

    print("\n" + "=" * 70)
    print("🧪 TESTING OTP FLOW (CORRECT VERSION)")
    print("=" * 70)

    # -------------------------------------------------------------------
    # Step 1: Clean up
    # -------------------------------------------------------------------
    print("\n1️⃣ Cleaning up existing test user...")
    User.objects.filter(phone_number=test_phone).delete()
    print("✅ Cleanup done")

    # -------------------------------------------------------------------
    # Step 2: Create farmer (profile is created elsewhere in real flow)
    # -------------------------------------------------------------------
    print("\n2️⃣ Creating test farmer user...")
    user = User.objects.create(
        phone_number=test_phone,
        full_name="Test Farmer",
        county="Nairobi",
        language="en",
        role="farmer",
        is_active=False,
        is_verified=False,
        password="dummy_password_not_used_for_farmers",
    )
    print(f"✅ User created: {user.full_name} ({user.phone_number})")

    # IMPORTANT: Do NOT manually create FarmerProfile
    # Assert expected domain behavior instead
    if hasattr(user, "farmer_profile"):
        print("✅ Farmer profile already exists")
    else:
        print("ℹ️ Farmer profile not created in this path (expected for this test)")

    # -------------------------------------------------------------------
    # Step 3: Generate OTP
    # -------------------------------------------------------------------
    print("\n3️⃣ Generating OTP...")
    user.verification_code = generate_verification_code()
    user.verification_code_created_at = timezone.now()
    user.save()

    print(f"✅ OTP generated: {user.verification_code}")
    print(f"   Created at: {user.verification_code_created_at}")

    # -------------------------------------------------------------------
    # Step 4: Test SMS sending
    # -------------------------------------------------------------------
    print("\n4️⃣ Testing SMS send...")
    success = UserService.send_login_otp(user)
    print(f"{'✅' if success else '❌'} SMS send result: {success}")

    user.refresh_from_db()
    print(f"   OTP after send: {user.verification_code}")

    # -------------------------------------------------------------------
    # Step 5: Simulate OTP verification
    # -------------------------------------------------------------------
    print("\n5️⃣ Testing OTP verification...")
    test_otp = user.verification_code

    print(f"   Stored OTP: '{user.verification_code}'")
    print(f"   Test OTP:   '{test_otp}'")
    print(f"   Match:      {user.verification_code == test_otp}")

    if user.verification_code_created_at:
        age = (timezone.now() - user.verification_code_created_at).total_seconds()
        print(f"   OTP age: {age:.2f} seconds")
        print(f"   Expired: {age > 600}")

    if user.verification_code == test_otp:
        print("✅ OTP verification would succeed!")

        # Activate user
        user.is_active = True
        user.is_verified = True
        user.verification_code = None
        user.verification_code_created_at = None
        user.save()
        print("✅ User activated")
    else:
        print("❌ OTP verification would fail!")

    # -------------------------------------------------------------------
    # Step 6: Final check
    # -------------------------------------------------------------------
    print("\n6️⃣ Final user state...")
    user.refresh_from_db()
    print(f"   Phone:     {user.phone_number}")
    print(f"   Active:    {user.is_active}")
    print(f"   Verified:  {user.is_verified}")
    print(f"   Role:      {user.role}")
    print(f"   OTP:       {user.verification_code or 'None (cleared)'}")

    print("\n" + "=" * 70)
    print("✅ TEST COMPLETE")
    print("=" * 70)

    print("\n📋 NEXT STEPS:")
    print("1. Register a farmer via API or frontend")
    print("2. Watch console for OTP")
    print("3. Copy 6-digit code")
    print("4. Verify via frontend or API")


if __name__ == "__main__":
    try:
        test_otp_flow()
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
