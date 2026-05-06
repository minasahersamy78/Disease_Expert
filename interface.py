"""
Expert System for Disease Diagnosis
Python Interface using PySwip

CLI:  python interface.py
Web: uvicorn api:app --reload   or   python api.py
"""

from __future__ import annotations

from typing import Any

from pyswip import Prolog
import os
import sys


def _resolve_prolog_path(prolog_file: str | None) -> str:
    """Resolve knowledge base path relative to this file when needed."""
    name = prolog_file or "expert_system.pl"
    if os.path.isabs(name):
        return name
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, name)


class DiseaseExpertSystem:
    def __init__(self, prolog_file: str | None = None, *, quiet: bool = False):
        """Initialize the expert system with Prolog knowledge base"""
        path = _resolve_prolog_path(prolog_file)
        self.prolog_file = path
        self.prolog = Prolog()

        if not os.path.exists(path):
            msg = f"[ERROR] {path} not found!"
            if not quiet:
                print(msg)
            raise FileNotFoundError(path)

        self.prolog.consult(path)
        if not quiet:
            print("[OK] Knowledge base loaded successfully!\n")

    def get_available_symptoms(self):
        """Get all available symptoms from the knowledge base"""
        symptoms = []
        for result in self.prolog.query("symptom(X)"):
            symptoms.append(result["X"])
        return symptoms

    def display_symptoms(self, symptoms):
        """Display symptoms in a numbered list"""
        print("Available Symptoms:")
        print("-" * 50)
        for idx, symptom in enumerate(symptoms, 1):
            formatted = symptom.replace("_", " ").title()
            print(f"{idx:2d}. {formatted}")
        print("-" * 50)

    def get_user_symptoms(self, available_symptoms):
        """Get symptoms from user input"""
        if not sys.stdin.isatty():
            print(
                "\nInteractive input is not available in this environment "
                "(e.g. Code Runner's Output panel is read-only)."
            )
            print("Fix: run in the integrated Terminal instead:")
            print("  cd to this folder, then:  python interface.py")
            print('Or set Code Runner: "code-runner.runInTerminal": true')
            raise SystemExit(1)

        print("\nEnter the numbers of symptoms you have (comma-separated):")
        print("Example: 1,3,5")

        while True:
            try:
                user_input = input("\nYour symptoms: ").strip()

                if not user_input:
                    print("Please enter at least one symptom number.")
                    continue

                indices = [int(x.strip()) for x in user_input.split(",")]

                if any(i < 1 or i > len(available_symptoms) for i in indices):
                    print(f"Please enter numbers between 1 and {len(available_symptoms)}")
                    continue

                selected = [available_symptoms[i - 1] for i in indices]
                return selected

            except ValueError:
                print("Invalid input! Please enter numbers separated by commas.")

    def diagnose(self, symptoms):
        """Query Prolog for possible diagnoses"""
        symptoms_str = "[" + ",".join(str(s) for s in symptoms) + "]"
        query = f"possible_diagnoses({symptoms_str}, Diagnoses)"
        results = list(self.prolog.query(query))
        return results

    def _has_exact_rule_match(self, symptoms):
        """True if at least one disease rule is fully satisfied (not overlap-only)."""
        symptoms_str = "[" + ",".join(str(s) for s in symptoms) + "]"
        q = f"diagnose(_, {symptoms_str}, _)"
        return bool(list(self.prolog.query(q)))

    def diagnosis_payload(self, results: list[Any], symptoms: list[str]) -> dict[str, Any]:
        """Structured result for JSON / web UI."""
        diagnoses_out: list[dict[str, str]] = []
        rows = (results[0].get("Diagnoses") if results else None) or []
        for disease, treatment in rows:
            d, t = str(disease), str(treatment)
            diagnoses_out.append(
                {
                    "disease": d,
                    "disease_display": d.replace("_", " ").title(),
                    "treatment": t,
                }
            )
        return {
            "symptoms": symptoms,
            "symptoms_display": [s.replace("_", " ").title() for s in symptoms],
            "exact_rule_match": self._has_exact_rule_match(symptoms),
            "diagnoses": diagnoses_out,
            "no_match": len(diagnoses_out) == 0,
        }

    def display_results(self, results, symptoms):
        """Display diagnosis results to user"""
        print("\n" + "=" * 70)
        print("DIAGNOSIS RESULTS")
        print("=" * 70)

        print("\nYour Symptoms:")
        for symptom in symptoms:
            print(f"  - {symptom.replace('_', ' ').title()}")

        print("\n" + "-" * 70)

        if not results or not results[0].get("Diagnoses"):
            print("\nWARNING: No conditions in the database match your symptoms well enough.")
            print("Try adding more symptoms, or consult a healthcare professional.")
        else:
            diagnoses = results[0]["Diagnoses"]
            if not self._has_exact_rule_match(symptoms):
                print(
                    "\nNOTE: No disease rule matched every required symptom. "
                    "Below are the closest matches (by overlapping symptoms), most likely first."
                )
            print(f"\nPossible Diagnoses: {len(diagnoses)} found\n")

            for idx, diagnosis in enumerate(diagnoses, 1):
                disease = diagnosis[0]
                treatment = diagnosis[1]

                disease_name = disease.replace("_", " ").title()

                print(f"{idx}. Disease: {disease_name}")
                print(f"   Treatment: {treatment}")
                print()

        print("=" * 70)
        print("\nDISCLAIMER: This is an educational expert system.")
        print("   Always consult a qualified healthcare professional for medical advice.")
        print("=" * 70)

    def run(self):
        """Main program loop"""
        print("\n" + "=" * 70)
        print("  EXPERT SYSTEM FOR DISEASE DIAGNOSIS")
        print("  AI406 - Knowledge Representation and Reasoning")
        print("=" * 70)

        while True:
            available_symptoms = self.get_available_symptoms()
            self.display_symptoms(available_symptoms)

            user_symptoms = self.get_user_symptoms(available_symptoms)

            print("\nAnalyzing symptoms...")
            results = self.diagnose(user_symptoms)

            self.display_results(results, user_symptoms)

            print("\n" + "-" * 70)
            again = input("\nWould you like to diagnose another case? (yes/no): ").strip().lower()
            if again not in ["yes", "y"]:
                print("\nThank you for using the Expert System. Stay healthy!")
                break
            print("\n")


def main():
    """Main entry point"""
    try:
        expert_system = DiseaseExpertSystem()
        expert_system.run()

    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
    except FileNotFoundError as e:
        print(f"\n[ERROR] Knowledge base missing: {e}")
    except Exception as e:
        print(f"\n[ERROR] An error occurred: {e}")
        print("Please make sure PySwip is installed correctly.")
        print("Install with: pip install pyswip")


if __name__ == "__main__":
    main()
