# --- 1. IMPORTS ---

# TestCase is the most important import. It lets you create a temporary,
# blank database for every test, so your real data is never touched.
from django.test import TestCase

# Import the models you need to create "fake" data for your tests.
from api.models import Order, User

# Import status codes (like 403 FORBIDDEN) to make your tests more readable
# than just using numbers.
from rest_framework import status

# 'reverse' is a helper that lets you find a URL by its 'name' (from urls.py)
# This is much safer than hard-coding the URL like '/api/my-orders/'.
from django.urls import reverse

# Create your tests here.

# --- 2. THE TEST SUITE ---


# This class is a "Test Suite" that groups all related tests.
# It must inherit from 'TestCase'.
class UserOrderTestCase(TestCase):

    # --- 3. THE "SETUP" METHOD ---

    # 'setUp' is a special method that runs *before* every single test
    # in this class. Its job is to "Arrange" the test data.
    def setUp(self):
        # Create two unique users.
        user1 = User.objects.create_user(username='user1', password='test')
        user2 = User.objects.create_user(username='user2', password='test')

        # Create 4 total orders in our temporary database.
        Order.objects.create(user=user1)  # 2 orders belong to user1
        Order.objects.create(user=user1)
        Order.objects.create(user=user2)  # 2 orders belong to user2
        Order.objects.create(user=user2)

    # --- 4. TEST 1: THE "HAPPY PATH" (AUTHENTICATED) ---

    # All test methods MUST start with 'test_'.
    # This test checks if a logged-in user gets *only* their own orders.
    def test_user_order_endpoint_retrieves_only_authenticated_user_orders(
            self):

        # --- Arrange (Get the user) ---
        # Get the user we created in setUp.
        user = User.objects.get(username='user1')

        # --- Arrange (Log in) ---
        # 'self.client' is a "fake browser."
        # We log in as 'user1' for this request.
        self.client.force_login(user)

        # --- Act (Make the API request) ---
        # We make a GET request to the URL named 'user-orders'.
        # 'self.client' is now acting as an authenticated 'user1'.
        response = self.client.get(reverse('user-orders'))

        # --- Assert (Check the results) ---
        # First, check if the page loaded successfully (HTTP 200).
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Convert the JSON response back into a Python list of dictionaries.
        orders = response.json()

        # This is the most important check!
        # It verifies that *every single order* in the response list
        # has a 'user' ID that matches 'user1'.
        # This proves our filtering logic in the view is working.
        self.assertTrue(all(order['user'] == user.id for order in orders))

        # We can also be more specific by checking the *count*.
        self.assertEqual(len(orders), 2)  # user1 only had 2 orders.

    # --- 5. TEST 2: THE "SAD PATH" (UNAUTHENTICATED) ---

    # This test checks if a "guest" (unauthenticated user) is
    # correctly blocked from seeing the page.
    def test_user_order_list_unauthenticated(self):

        # --- Act (Make the API request) ---
        # We make the same GET request, but this time we *do not* log in.
        # 'self.client' is acting as an anonymous "guest".
        response = self.client.get(reverse('user-orders'))

        # --- Assert (Check the results) ---
        # We *expect* to be denied.
        # We check that the server returned a "Forbidden" (403) status code,
        # proving our API security (e.g., IsAuthenticated) is working.
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
