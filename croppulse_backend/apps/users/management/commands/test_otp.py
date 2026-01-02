"""
Django management command to test OTP flow
Save as: apps/users/management/commands/test_otp.py

Create directories if they don't exist:
mkdir -p apps/users/management/commands
touch apps/users/management/__init__.py
touch apps/users/management/commands/__init__.py
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.users.models import User, FarmerProfile
from apps.users.services import UserService
from core.utils import generate_verification_code
import json


class Command(BaseCommand):
    help = 'Test OTP flow for farmer authentication'

    def add_arguments(self, parser):
        parser.add_argument(
            '--phone',
            type=str,
            default='+254712345678',
            help='Phone number to test with'
        )
        parser.add_argument(
            '--action',
            type=str,
            choices=['create', 'send', 'verify', 'check', 'delete'],
            default='create',
            help='Action to perform'
        )
        parser.add_argument(
            '--otp',
            type=str,
            help='OTP code for verification'
        )

    def handle(self, *args, **options):
        phone = options['phone']
        action = options['action']
        
        self.stdout.write(self.style.SUCCESS(f'\n{"="*70}'))
        self.stdout.write(self.style.SUCCESS(f'Testing OTP Flow - Action: {action}'))
        self.stdout.write(self.style.SUCCESS(f'{"="*70}\n'))

        if action == 'create':
            self.create_test_farmer(phone)
        elif action == 'send':
            self.send_otp(phone)
        elif action == 'verify':
            if not options['otp']:
                self.stdout.write(self.style.ERROR('❌ --otp required for verify action'))
                return
            self.verify_otp(phone, options['otp'])
        elif action == 'check':
            self.check_farmer(phone)
        elif action == 'delete':
            self.delete_farmer(phone)

    def create_test_farmer(self, phone):
        """Create a test farmer"""
        try:
            # Delete existing if present
            User.objects.filter(phone_number=phone).delete()
            
            # Generate OTP
            otp = generate_verification_code()
            
            # Create user
            user = User.objects.create(
                phone_number=phone,
                full_name='Test Farmer',
                county='Nairobi',
                language='en',
                role='farmer',
                is_active=False,
                verification_code=otp,
                verification_code_created_at=timezone.now()
            )
            
            # Create farmer profile
            FarmerProfile.objects.create(
                user=user,
                farm_size=0,
                primary_crop='maize'
            )
            
            self.stdout.write(self.style.SUCCESS(f'✅ Test farmer created'))
            self.stdout.write(self.style.SUCCESS(f'Phone: {phone}'))
            self.stdout.write(self.style.SUCCESS(f'OTP: {otp}'))
            self.stdout.write(self.style.SUCCESS(f'Created at: {user.verification_code_created_at}'))
            
            # Test sending SMS
            self.stdout.write(self.style.WARNING('\n📤 Testing SMS send...'))
            success = UserService.send_login_otp(user)
            self.stdout.write(self.style.SUCCESS(f'SMS send result: {success}'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))

    def send_otp(self, phone):
        """Send OTP to existing farmer"""
        try:
            user = User.objects.get(phone_number=phone, role='farmer')
            
            # Generate new OTP
            user.verification_code = generate_verification_code()
            user.verification_code_created_at = timezone.now()
            user.save()
            
            self.stdout.write(self.style.SUCCESS(f'✅ Generated new OTP: {user.verification_code}'))
            
            # Send SMS
            success = UserService.send_login_otp(user)
            self.stdout.write(self.style.SUCCESS(f'📤 SMS send result: {success}'))
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ Farmer not found: {phone}'))

    def verify_otp(self, phone, otp):
        """Verify OTP"""
        try:
            user = User.objects.get(phone_number=phone, role='farmer')
            
            self.stdout.write(f'Stored OTP: {user.verification_code}')
            self.stdout.write(f'Provided OTP: {otp}')
            self.stdout.write(f'Match: {user.verification_code == otp}')
            
            if user.verification_code != otp:
                self.stdout.write(self.style.ERROR('❌ OTP does not match'))
                return
            
            # Check expiration
            if user.verification_code_created_at:
                elapsed = timezone.now() - user.verification_code_created_at
                seconds = elapsed.total_seconds()
                self.stdout.write(f'OTP age: {seconds} seconds')
                
                if seconds > 600:
                    self.stdout.write(self.style.ERROR('❌ OTP expired (>10 minutes)'))
                    return
            
            self.stdout.write(self.style.SUCCESS('✅ OTP is valid!'))
            
            # Activate user
            user.is_active = True
            user.is_verified = True
            user.verification_code = None
            user.verification_code_created_at = None
            user.save()
            
            self.stdout.write(self.style.SUCCESS('✅ User activated and verified'))
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ Farmer not found: {phone}'))

    def check_farmer(self, phone):
        """Check farmer details"""
        try:
            user = User.objects.get(phone_number=phone)
            
            self.stdout.write(self.style.SUCCESS(f'✅ Farmer found'))
            self.stdout.write(f'ID: {user.id}')
            self.stdout.write(f'Phone: {user.phone_number}')
            self.stdout.write(f'Name: {user.full_name}')
            self.stdout.write(f'Role: {user.role}')
            self.stdout.write(f'Active: {user.is_active}')
            self.stdout.write(f'Verified: {user.is_verified}')
            self.stdout.write(f'OTP: {user.verification_code or "None"}')
            self.stdout.write(f'OTP Created: {user.verification_code_created_at or "None"}')
            
            if user.verification_code_created_at:
                elapsed = timezone.now() - user.verification_code_created_at
                self.stdout.write(f'OTP Age: {elapsed.total_seconds()} seconds')
            
            # Check farmer profile
            try:
                profile = user.farmer_profile
                self.stdout.write(f'\nFarmer Profile:')
                self.stdout.write(f'  Farm: {profile.farm_name or "Not set"}')
                self.stdout.write(f'  Size: {profile.farm_size} hectares')
                self.stdout.write(f'  Crop: {profile.primary_crop}')
            except:
                self.stdout.write(self.style.WARNING('⚠️ No farmer profile'))
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ Farmer not found: {phone}'))

    def delete_farmer(self, phone):
        """Delete test farmer"""
        try:
            user = User.objects.get(phone_number=phone)
            user.delete()
            self.stdout.write(self.style.SUCCESS(f'✅ Deleted farmer: {phone}'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ Farmer not found: {phone}'))