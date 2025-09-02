#!/usr/bin/env python3
"""
Backend API Testing Suite for Activity Management System
Tests all backend endpoints according to test_result.md requirements
"""

import requests
import json
import uuid
from datetime import datetime, timezone, timedelta
import sys
import os

# Configuration
BASE_URL = "https://manage-tasks-1.preview.emergentagent.com/api"
TEST_USERNAME = f"testuser_{uuid.uuid4().hex[:8]}"
TEST_EMAIL = f"test_{uuid.uuid4().hex[:8]}@example.com"
TEST_PASSWORD = "SecurePassword123!"

class ActivityTestSuite:
    def __init__(self):
        self.base_url = BASE_URL
        self.auth_token = None
        self.user_data = None
        self.test_activity_id = None
        self.results = {
            "authentication": {"passed": 0, "failed": 0, "details": []},
            "crud_operations": {"passed": 0, "failed": 0, "details": []},
            "categories_status": {"passed": 0, "failed": 0, "details": []},
            "dashboard_stats": {"passed": 0, "failed": 0, "details": []},
            "mongodb_integration": {"passed": 0, "failed": 0, "details": []}
        }
    
    def log_result(self, category, test_name, passed, details=""):
        """Log test result"""
        if passed:
            self.results[category]["passed"] += 1
            status = "✅ PASS"
        else:
            self.results[category]["failed"] += 1
            status = "❌ FAIL"
        
        self.results[category]["details"].append(f"{status}: {test_name} - {details}")
        print(f"{status}: {test_name} - {details}")
    
    def test_user_registration(self):
        """Test user registration endpoint"""
        print("\n=== Testing User Registration ===")
        
        try:
            payload = {
                "username": TEST_USERNAME,
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD
            }
            
            response = requests.post(f"{self.base_url}/auth/register", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data and "user" in data:
                    self.auth_token = data["access_token"]
                    self.user_data = data["user"]
                    self.log_result("authentication", "User Registration", True, 
                                  f"User {TEST_USERNAME} registered successfully with token")
                    return True
                else:
                    self.log_result("authentication", "User Registration", False, 
                                  "Missing access_token or user in response")
                    return False
            else:
                self.log_result("authentication", "User Registration", False, 
                              f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("authentication", "User Registration", False, f"Exception: {str(e)}")
            return False
    
    def test_user_login(self):
        """Test user login endpoint"""
        print("\n=== Testing User Login ===")
        
        try:
            payload = {
                "username": TEST_USERNAME,
                "password": TEST_PASSWORD
            }
            
            response = requests.post(f"{self.base_url}/auth/login", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data and "user" in data:
                    # Update token from login
                    self.auth_token = data["access_token"]
                    self.log_result("authentication", "User Login", True, 
                                  f"Login successful for {TEST_USERNAME}")
                    return True
                else:
                    self.log_result("authentication", "User Login", False, 
                                  "Missing access_token or user in response")
                    return False
            else:
                self.log_result("authentication", "User Login", False, 
                              f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("authentication", "User Login", False, f"Exception: {str(e)}")
            return False
    
    def test_invalid_login(self):
        """Test login with invalid credentials"""
        print("\n=== Testing Invalid Login ===")
        
        try:
            payload = {
                "username": TEST_USERNAME,
                "password": "wrongpassword"
            }
            
            response = requests.post(f"{self.base_url}/auth/login", json=payload)
            
            if response.status_code == 401:
                self.log_result("authentication", "Invalid Login Rejection", True, 
                              "Correctly rejected invalid credentials")
                return True
            else:
                self.log_result("authentication", "Invalid Login Rejection", False, 
                              f"Expected 401, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("authentication", "Invalid Login Rejection", False, f"Exception: {str(e)}")
            return False
    
    def get_auth_headers(self):
        """Get authorization headers"""
        if not self.auth_token:
            return {}
        return {"Authorization": f"Bearer {self.auth_token}"}
    
    def test_protected_endpoint_without_auth(self):
        """Test that protected endpoints require authentication"""
        print("\n=== Testing Protected Endpoint Security ===")
        
        try:
            response = requests.get(f"{self.base_url}/activities")
            
            if response.status_code == 403:
                self.log_result("authentication", "Protected Endpoint Security", True, 
                              "Correctly rejected request without authentication")
                return True
            else:
                self.log_result("authentication", "Protected Endpoint Security", False, 
                              f"Expected 403, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("authentication", "Protected Endpoint Security", False, f"Exception: {str(e)}")
            return False
    
    def test_create_activity(self):
        """Test activity creation"""
        print("\n=== Testing Activity Creation ===")
        
        try:
            payload = {
                "title": "Test Activity for Backend Testing",
                "description": "This is a comprehensive test activity",
                "category": "Trabalho",
                "status": "pending",
                "priority": "high",
                "due_date": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
            }
            
            response = requests.post(f"{self.base_url}/activities", 
                                   json=payload, headers=self.get_auth_headers())
            
            if response.status_code == 200:
                data = response.json()
                if "id" in data and data["title"] == payload["title"]:
                    self.test_activity_id = data["id"]
                    self.log_result("crud_operations", "Activity Creation", True, 
                                  f"Activity created with ID: {self.test_activity_id}")
                    return True
                else:
                    self.log_result("crud_operations", "Activity Creation", False, 
                                  "Missing ID or incorrect title in response")
                    return False
            else:
                self.log_result("crud_operations", "Activity Creation", False, 
                              f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("crud_operations", "Activity Creation", False, f"Exception: {str(e)}")
            return False
    
    def test_get_activities(self):
        """Test getting all activities"""
        print("\n=== Testing Get All Activities ===")
        
        try:
            response = requests.get(f"{self.base_url}/activities", headers=self.get_auth_headers())
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    self.log_result("crud_operations", "Get All Activities", True, 
                                  f"Retrieved {len(data)} activities")
                    return True
                else:
                    self.log_result("crud_operations", "Get All Activities", True, 
                                  "Retrieved empty activity list (valid)")
                    return True
            else:
                self.log_result("crud_operations", "Get All Activities", False, 
                              f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("crud_operations", "Get All Activities", False, f"Exception: {str(e)}")
            return False
    
    def test_get_single_activity(self):
        """Test getting a single activity"""
        print("\n=== Testing Get Single Activity ===")
        
        if not self.test_activity_id:
            self.log_result("crud_operations", "Get Single Activity", False, 
                          "No test activity ID available")
            return False
        
        try:
            response = requests.get(f"{self.base_url}/activities/{self.test_activity_id}", 
                                  headers=self.get_auth_headers())
            
            if response.status_code == 200:
                data = response.json()
                if data["id"] == self.test_activity_id:
                    self.log_result("crud_operations", "Get Single Activity", True, 
                                  f"Retrieved activity {self.test_activity_id}")
                    return True
                else:
                    self.log_result("crud_operations", "Get Single Activity", False, 
                                  "Activity ID mismatch in response")
                    return False
            else:
                self.log_result("crud_operations", "Get Single Activity", False, 
                              f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("crud_operations", "Get Single Activity", False, f"Exception: {str(e)}")
            return False
    
    def test_update_activity(self):
        """Test updating an activity"""
        print("\n=== Testing Activity Update ===")
        
        if not self.test_activity_id:
            self.log_result("crud_operations", "Activity Update", False, 
                          "No test activity ID available")
            return False
        
        try:
            payload = {
                "title": "Updated Test Activity",
                "status": "in_progress",
                "priority": "medium"
            }
            
            response = requests.put(f"{self.base_url}/activities/{self.test_activity_id}", 
                                  json=payload, headers=self.get_auth_headers())
            
            if response.status_code == 200:
                data = response.json()
                if data["title"] == payload["title"] and data["status"] == payload["status"]:
                    self.log_result("crud_operations", "Activity Update", True, 
                                  f"Activity {self.test_activity_id} updated successfully")
                    return True
                else:
                    self.log_result("crud_operations", "Activity Update", False, 
                                  "Update data not reflected in response")
                    return False
            else:
                self.log_result("crud_operations", "Activity Update", False, 
                              f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("crud_operations", "Activity Update", False, f"Exception: {str(e)}")
            return False
    
    def test_activity_categories(self):
        """Test activity categories"""
        print("\n=== Testing Activity Categories ===")
        
        categories = ["Geral", "Trabalho", "Pessoal", "Estudos", "Saúde"]
        
        for category in categories:
            try:
                payload = {
                    "title": f"Test {category} Activity",
                    "description": f"Testing {category} category",
                    "category": category,
                    "status": "pending",
                    "priority": "low"
                }
                
                response = requests.post(f"{self.base_url}/activities", 
                                       json=payload, headers=self.get_auth_headers())
                
                if response.status_code == 200:
                    data = response.json()
                    if data["category"] == category:
                        self.log_result("categories_status", f"Category {category}", True, 
                                      f"Successfully created activity with category {category}")
                    else:
                        self.log_result("categories_status", f"Category {category}", False, 
                                      f"Category mismatch: expected {category}, got {data.get('category')}")
                else:
                    self.log_result("categories_status", f"Category {category}", False, 
                                  f"HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                self.log_result("categories_status", f"Category {category}", False, f"Exception: {str(e)}")
    
    def test_activity_statuses(self):
        """Test activity status tracking"""
        print("\n=== Testing Activity Status Tracking ===")
        
        statuses = ["pending", "in_progress", "completed"]
        
        for status in statuses:
            try:
                payload = {
                    "title": f"Test {status} Activity",
                    "description": f"Testing {status} status",
                    "category": "Geral",
                    "status": status,
                    "priority": "medium"
                }
                
                response = requests.post(f"{self.base_url}/activities", 
                                       json=payload, headers=self.get_auth_headers())
                
                if response.status_code == 200:
                    data = response.json()
                    if data["status"] == status:
                        self.log_result("categories_status", f"Status {status}", True, 
                                      f"Successfully created activity with status {status}")
                    else:
                        self.log_result("categories_status", f"Status {status}", False, 
                                      f"Status mismatch: expected {status}, got {data.get('status')}")
                else:
                    self.log_result("categories_status", f"Status {status}", False, 
                                  f"HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                self.log_result("categories_status", f"Status {status}", False, f"Exception: {str(e)}")
    
    def test_dashboard_statistics(self):
        """Test dashboard statistics endpoint"""
        print("\n=== Testing Dashboard Statistics ===")
        
        try:
            response = requests.get(f"{self.base_url}/activities/stats/dashboard", 
                                  headers=self.get_auth_headers())
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["total", "completed", "pending", "in_progress"]
                
                if all(field in data for field in required_fields):
                    self.log_result("dashboard_stats", "Dashboard Statistics", True, 
                                  f"Stats: Total={data['total']}, Completed={data['completed']}, "
                                  f"Pending={data['pending']}, In Progress={data['in_progress']}")
                    return True
                else:
                    missing_fields = [field for field in required_fields if field not in data]
                    self.log_result("dashboard_stats", "Dashboard Statistics", False, 
                                  f"Missing fields: {missing_fields}")
                    return False
            else:
                self.log_result("dashboard_stats", "Dashboard Statistics", False, 
                              f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("dashboard_stats", "Dashboard Statistics", False, f"Exception: {str(e)}")
            return False
    
    def test_delete_activity(self):
        """Test activity deletion"""
        print("\n=== Testing Activity Deletion ===")
        
        if not self.test_activity_id:
            self.log_result("crud_operations", "Activity Deletion", False, 
                          "No test activity ID available")
            return False
        
        try:
            response = requests.delete(f"{self.base_url}/activities/{self.test_activity_id}", 
                                     headers=self.get_auth_headers())
            
            if response.status_code == 200:
                # Verify deletion by trying to get the activity
                get_response = requests.get(f"{self.base_url}/activities/{self.test_activity_id}", 
                                          headers=self.get_auth_headers())
                
                if get_response.status_code == 404:
                    self.log_result("crud_operations", "Activity Deletion", True, 
                                  f"Activity {self.test_activity_id} deleted successfully")
                    return True
                else:
                    self.log_result("crud_operations", "Activity Deletion", False, 
                                  "Activity still exists after deletion")
                    return False
            else:
                self.log_result("crud_operations", "Activity Deletion", False, 
                              f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("crud_operations", "Activity Deletion", False, f"Exception: {str(e)}")
            return False
    
    def test_mongodb_integration(self):
        """Test MongoDB integration by verifying data persistence"""
        print("\n=== Testing MongoDB Integration ===")
        
        try:
            # Create an activity
            payload = {
                "title": "MongoDB Integration Test",
                "description": "Testing data persistence",
                "category": "Estudos",
                "status": "pending",
                "priority": "high"
            }
            
            create_response = requests.post(f"{self.base_url}/activities", 
                                          json=payload, headers=self.get_auth_headers())
            
            if create_response.status_code == 200:
                activity_data = create_response.json()
                activity_id = activity_data["id"]
                
                # Retrieve the activity to verify persistence
                get_response = requests.get(f"{self.base_url}/activities/{activity_id}", 
                                          headers=self.get_auth_headers())
                
                if get_response.status_code == 200:
                    retrieved_data = get_response.json()
                    
                    # Verify data integrity
                    if (retrieved_data["title"] == payload["title"] and 
                        retrieved_data["category"] == payload["category"]):
                        self.log_result("mongodb_integration", "Data Persistence", True, 
                                      "Data correctly persisted and retrieved from MongoDB")
                        
                        # Clean up
                        requests.delete(f"{self.base_url}/activities/{activity_id}", 
                                      headers=self.get_auth_headers())
                        return True
                    else:
                        self.log_result("mongodb_integration", "Data Persistence", False, 
                                      "Data integrity issue - retrieved data doesn't match")
                        return False
                else:
                    self.log_result("mongodb_integration", "Data Persistence", False, 
                                  f"Failed to retrieve activity: HTTP {get_response.status_code}")
                    return False
            else:
                self.log_result("mongodb_integration", "Data Persistence", False, 
                              f"Failed to create activity: HTTP {create_response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("mongodb_integration", "Data Persistence", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting Backend API Test Suite")
        print(f"Testing against: {self.base_url}")
        print(f"Test User: {TEST_USERNAME}")
        print("=" * 60)
        
        # Authentication Tests
        if not self.test_user_registration():
            print("❌ Registration failed - cannot continue with other tests")
            return False
        
        self.test_user_login()
        self.test_invalid_login()
        self.test_protected_endpoint_without_auth()
        
        # CRUD Operations Tests
        self.test_create_activity()
        self.test_get_activities()
        self.test_get_single_activity()
        self.test_update_activity()
        
        # Categories and Status Tests
        self.test_activity_categories()
        self.test_activity_statuses()
        
        # Dashboard Statistics Tests
        self.test_dashboard_statistics()
        
        # MongoDB Integration Tests
        self.test_mongodb_integration()
        
        # Cleanup - Delete test activity if it exists
        if self.test_activity_id:
            self.test_delete_activity()
        
        # Print Summary
        self.print_summary()
        
        return self.get_overall_success()
    
    def print_summary(self):
        """Print test results summary"""
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        total_passed = 0
        total_failed = 0
        
        for category, results in self.results.items():
            passed = results["passed"]
            failed = results["failed"]
            total_passed += passed
            total_failed += failed
            
            status = "✅" if failed == 0 else "❌"
            print(f"{status} {category.replace('_', ' ').title()}: {passed} passed, {failed} failed")
            
            # Print details for failed tests
            if failed > 0:
                for detail in results["details"]:
                    if "❌ FAIL" in detail:
                        print(f"    {detail}")
        
        print("-" * 60)
        print(f"OVERALL: {total_passed} passed, {total_failed} failed")
        
        if total_failed == 0:
            print("🎉 ALL TESTS PASSED!")
        else:
            print(f"⚠️  {total_failed} TESTS FAILED")
    
    def get_overall_success(self):
        """Check if all tests passed"""
        total_failed = sum(results["failed"] for results in self.results.values())
        return total_failed == 0

def main():
    """Main test execution"""
    test_suite = ActivityTestSuite()
    success = test_suite.run_all_tests()
    
    if success:
        print("\n✅ Backend testing completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Backend testing completed with failures!")
        sys.exit(1)

if __name__ == "__main__":
    main()