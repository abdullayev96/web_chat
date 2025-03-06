import requests
import http.client
import json
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from django_private_chat2.models import User
from django.db.utils import IntegrityError



def e_tokens():
    try:
        conn = http.client.HTTPConnection("edo-api.loc", timeout=60)

        payload = json.dumps({
            "email": "admin@turonbank.uz",
            "password": "123456"
        })
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        conn.request("POST", "/api/login", payload, headers)
        res = conn.getresponse()
        print(f"Response status: {res.status}, reason: {res.reason}")

        if res.status == 200:
            data = res.read()
            try:
                token_data = json.loads(data.decode("utf-8"))
                print(f"Token data: {token_data}")
                return token_data.get("access_token")
            except json.JSONDecodeError:
                print(f"Invalid response format: {data}")
        else:
            print(f"Failed to fetch token: {res.status} - {res.reason}")
    except Exception as e:
        print(f"Error fetching token: {e}")
    return None





DEFAULT_PASSWORD = "default123"

class Command(BaseCommand):
    help = "Fetch and save users from the API"

    def generate_unique_username(self, first_name, last_name, per_id):
        base_username = f"{first_name}.{last_name}".lower().replace(" ", "_")
        username = base_username
        count = 1

        while User.objects.filter(username=username).exists():
            username = f"{base_username}{count}"
            count += 1

        return username

    def handle(self, *args, **kwargs):
        token = e_tokens()
        if not token:
            self.stderr.write("Failed to fetch authentication token.")
            return

        try:
            conn = http.client.HTTPConnection("edo-api.loc")
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-type': 'application/json'
            }

            conn.request("GET", "/api/v1/users", headers=headers)
            res = conn.getresponse()
            print(f"Fetching users: Response status {res.status}, reason: {res.reason}")

            if res.status == 200:
                data = res.read()
                users = json.loads(data.decode("utf-8"))
                print("Fetched users:", users)

                for user_data in users:
                    first_name = user_data["first_name"]
                    last_name = user_data["last_name"]
                    per_id = user_data["per_id"]

                    username = self.generate_unique_username(first_name, last_name, per_id)

                    try:
                        user, created = User.objects.update_or_create(
                            per_id=per_id,
                            defaults={
                                "username": username,
                                "last_name": last_name,
                                "first_name": first_name,
                                "middle_name": user_data.get("middle_name"),
                                "dep_id": user_data["dep_id"],
                                "department": user_data["department"],
                                "position": user_data["position"],
                                "tab_number": user_data["tab_number"],
                                "per_status": user_data["per_status"],
                                "phone_number": user_data.get("phone_number"),
                                "ip_phone": user_data.get("ip_phone"),
                                "birthday": parse_date(user_data["birthday"]) if user_data["birthday"] else None,
                                "gender_code": user_data.get("gender_code"),
                            },
                        )

                        # Set a default password for newly created users
                        if created:
                            user.set_password(DEFAULT_PASSWORD)
                            user.is_staff = True
                            user.save()

                        status = "Created" if created else "Updated"
                        print(f"User {username} ({status}) successfully.")

                    except IntegrityError as e:
                        print(f"Skipping user {username} due to IntegrityError: {e}")

                self.stdout.write(self.style.SUCCESS("Users successfully saved/updated."))
            else:
                self.stderr.write(f"Failed to fetch users. Status: {res.status} - {res.reason}")

        except Exception as e:
            self.stderr.write(f"Unexpected error: {e}")




#
#
# class Command(BaseCommand):
#     help = "Fetch and save users from the API"
#
#     def handle(self, *args, **kwargs):
#
#         token = e_tokens()
#         if not token:
#             self.stderr.write("Failed to fetch authentication token.")
#             return
#
#         try:
#             conn = http.client.HTTPConnection("edo-api.loc")
#             headers = {
#                 'Authorization': f'Bearer {token}',
#                 'Content-type': 'application/json'
#             }
#
#             conn.request("GET", "/api/v1/users", headers=headers)
#             res = conn.getresponse()
#             print(f"Fetching users: Response status {res.status}, reason: {res.reason}")
#
#             if res.status == 200:
#                 data = res.read()
#                 users = json.loads(data.decode("utf-8"))
#                 print("Fetched users:", users)
#
#                 for user_data in users:
#                     #username = f"user_{user_data['per_id']}"
#                     username = f"{user_data['first_name']}.{user_data['last_name']}"
#
#                     User.objects.update_or_create(
#                         per_id=user_data["per_id"],
#                         defaults={
#                             "username": username,
#                             "last_name": user_data["last_name"],
#                             "first_name": user_data["first_name"],
#                             "middle_name": user_data.get("middle_name"),
#                             "dep_id": user_data["dep_id"],
#                             "department": user_data["department"],
#                             "position": user_data["position"],
#                             "tab_number": user_data["tab_number"],
#                             "per_status": user_data["per_status"],
#                             "phone_number": user_data.get("phone_number"),
#                             "ip_phone": user_data.get("ip_phone"),
#                             "birthday": parse_date(user_data["birthday"]) if user_data["birthday"] else None,
#                             "gender_code": user_data.get("gender_code"),
#                         },
#                     )
#                 self.stdout.write(self.style.SUCCESS("Users successfully saved/updated."))
#             else:
#                 self.stderr.write(f"Failed to fetch users. Status: {res.status} - {res.reason}")
#
#         except Exception as e:
#             self.stderr.write(f"Unexpected error: {e}")
#


