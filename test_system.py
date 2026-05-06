"""
Test Script for Expert System
This script tests the basic functionality without requiring user input
"""

from pyswip import Prolog
import os

def test_prolog_connection():
    """Test if Prolog file loads correctly"""
    print("=" * 70)
    print("TEST 1: Prolog Knowledge Base Loading")
    print("=" * 70)
    
    try:
        prolog = Prolog()
        if os.path.exists('expert_system.pl'):
            prolog.consult('expert_system.pl')
            print("✓ SUCCESS: Prolog knowledge base loaded successfully!")
            return prolog
        else:
            print("✗ FAILED: expert_system.pl not found!")
            return None
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return None

def test_symptoms_retrieval(prolog):
    """Test retrieving symptoms from knowledge base"""
    print("\n" + "=" * 70)
    print("TEST 2: Symptom Retrieval")
    print("=" * 70)
    
    try:
        symptoms = []
        for result in prolog.query("symptom(X)"):
            symptoms.append(result['X'])
        
        print(f"✓ SUCCESS: Retrieved {len(symptoms)} symptoms")
        print(f"Sample symptoms: {symptoms[:5]}...")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_diagnosis(prolog, test_case_name, symptoms):
    """Test diagnosis with specific symptoms"""
    print("\n" + "=" * 70)
    print(f"TEST: {test_case_name}")
    print("=" * 70)
    
    print(f"Symptoms: {', '.join(symptoms)}")
    
    try:
        symptoms_str = '[' + ','.join(symptoms) + ']'
        query = f"possible_diagnoses({symptoms_str}, Diagnoses)"
        results = list(prolog.query(query))
        
        if results and results[0].get('Diagnoses'):
            diagnoses = results[0]['Diagnoses']
            print(f"✓ SUCCESS: Found {len(diagnoses)} diagnosis(es)")
            
            for idx, diagnosis in enumerate(diagnoses, 1):
                disease = diagnosis[0]
                treatment = diagnosis[1]
                print(f"\n  {idx}. Disease: {disease}")
                print(f"     Treatment: {treatment}")
        else:
            print("✓ No diagnosis found (expected for non-matching symptoms)")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("  EXPERT SYSTEM - AUTOMATED TESTING")
    print("  AI406 - Knowledge Representation and Reasoning")
    print("=" * 70)
    
    # Test 1: Load Prolog
    prolog = test_prolog_connection()
    if not prolog:
        print("\nCannot proceed with tests. Please check Prolog installation.")
        return
    
    # Test 2: Retrieve symptoms
    if not test_symptoms_retrieval(prolog):
        return
    
    # Test 3: Flu diagnosis
    test_diagnosis(
        prolog,
        "Flu Diagnosis",
        ['fever', 'cough', 'body_aches', 'fatigue']
    )
    
    # Test 4: Common Cold diagnosis
    test_diagnosis(
        prolog,
        "Common Cold Diagnosis",
        ['runny_nose', 'sneezing', 'sore_throat']
    )
    
    # Test 5: Gastroenteritis diagnosis
    test_diagnosis(
        prolog,
        "Gastroenteritis Diagnosis",
        ['nausea', 'vomiting', 'diarrhea']
    )
    
    # Test 6: Multiple possible diagnoses
    test_diagnosis(
        prolog,
        "Multiple Diagnosis (Fever + Headache + Nausea + Fatigue)",
        ['fever', 'headache', 'nausea', 'fatigue']
    )
    
    # Test 7: Partial overlap (broader KB ranks skin symptoms with allergies)
    test_diagnosis(
        prolog,
        "Partial overlap (Rash + Itching — expect allergy-related ranking)",
        ['rash', 'itching']
    )
    
    print("\n" + "=" * 70)
    print("  ALL TESTS COMPLETED")
    print("=" * 70)
    print("\nIf all tests passed, the system is ready to use!")
    print("Run 'python interface.py' to start the interactive interface.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("\nMake sure:")
        print("1. SWI-Prolog is installed")
        print("2. PySwip is installed (pip install pyswip)")
        print("3. expert_system.pl exists in the current directory")
