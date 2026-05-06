% Expert System for Disease Diagnosis
% Knowledge Base with Facts and Rules

% Symptoms facts
symptom(fever).
symptom(cough).
symptom(headache).
symptom(sore_throat).
symptom(runny_nose).
symptom(fatigue).
symptom(body_aches).
symptom(chest_pain).
symptom(shortness_of_breath).
symptom(nausea).
symptom(vomiting).
symptom(diarrhea).
symptom(stomach_pain).
symptom(rash).
symptom(itching).
symptom(sneezing).
symptom(watery_eyes).

% Broader signature lists for overlap ranking (not strict clinical criteria; demo KB).
% Include rash/itching where skin or systemic illness overlap is plausible so more combinations match.
disease_signature(common_cold, [runny_nose, sneezing, sore_throat, cough, fatigue]).
disease_signature(flu, [fever, cough, body_aches, fatigue, headache, rash]).
disease_signature(covid19, [fever, cough, fatigue, shortness_of_breath, body_aches, headache, rash]).
disease_signature(bronchitis, [cough, chest_pain, fatigue, fever]).
disease_signature(gastroenteritis, [nausea, vomiting, diarrhea, stomach_pain, fever]).
disease_signature(food_poisoning, [nausea, vomiting, stomach_pain, diarrhea, fever]).
disease_signature(allergies, [sneezing, runny_nose, watery_eyes, itching, rash]).
disease_signature(migraine, [headache, nausea, fatigue, vomiting]).
disease_signature(strep_throat, [sore_throat, fever, headache, body_aches, rash]).
disease_signature(heat_exhaustion, [fever, headache, nausea, fatigue, rash]).

treatment_text(common_cold, 'Rest, drink fluids, and take over-the-counter cold medicine').
treatment_text(flu, 'Rest, drink plenty of fluids, take antiviral medication if prescribed, and manage fever').
treatment_text(covid19, 'Isolate, rest, monitor oxygen levels, seek medical attention if breathing difficulty').
treatment_text(bronchitis, 'Rest, drink fluids, use humidifier, may need antibiotics if bacterial').
treatment_text(gastroenteritis, 'Stay hydrated, eat bland foods, rest, avoid dairy temporarily').
treatment_text(food_poisoning, 'Stay hydrated, rest, avoid solid food initially, seek help if severe').
treatment_text(allergies, 'Take antihistamines, avoid allergens, use nasal spray if needed').
treatment_text(migraine, 'Rest in dark room, take pain relievers, stay hydrated, avoid triggers').
treatment_text(strep_throat, 'See doctor for antibiotics, rest, drink warm liquids, gargle salt water').
treatment_text(heat_exhaustion, 'Move to cool place, drink water, rest, cool down body temperature').

% Exact diagnosis (original rule logic)
diagnose(common_cold, Symptoms, T) :-
    treatment_text(common_cold, T),
    member(runny_nose, Symptoms),
    member(sneezing, Symptoms),
    member(sore_throat, Symptoms).

diagnose(flu, Symptoms, T) :-
    treatment_text(flu, T),
    member(fever, Symptoms),
    member(cough, Symptoms),
    member(body_aches, Symptoms),
    member(fatigue, Symptoms).

diagnose(covid19, Symptoms, T) :-
    treatment_text(covid19, T),
    member(fever, Symptoms),
    member(cough, Symptoms),
    member(fatigue, Symptoms),
    (member(shortness_of_breath, Symptoms); member(body_aches, Symptoms)).

diagnose(bronchitis, Symptoms, T) :-
    treatment_text(bronchitis, T),
    member(cough, Symptoms),
    member(chest_pain, Symptoms),
    member(fatigue, Symptoms).

diagnose(gastroenteritis, Symptoms, T) :-
    treatment_text(gastroenteritis, T),
    member(nausea, Symptoms),
    member(vomiting, Symptoms),
    member(diarrhea, Symptoms).

diagnose(food_poisoning, Symptoms, T) :-
    treatment_text(food_poisoning, T),
    member(nausea, Symptoms),
    member(vomiting, Symptoms),
    member(stomach_pain, Symptoms),
    member(diarrhea, Symptoms).

diagnose(allergies, Symptoms, T) :-
    treatment_text(allergies, T),
    member(sneezing, Symptoms),
    member(runny_nose, Symptoms),
    member(watery_eyes, Symptoms),
    member(itching, Symptoms).

diagnose(migraine, Symptoms, T) :-
    treatment_text(migraine, T),
    member(headache, Symptoms),
    member(nausea, Symptoms),
    (member(fatigue, Symptoms); member(sensitivity_to_light, Symptoms)).

diagnose(strep_throat, Symptoms, T) :-
    treatment_text(strep_throat, T),
    member(sore_throat, Symptoms),
    member(fever, Symptoms),
    (member(headache, Symptoms); member(body_aches, Symptoms)).

diagnose(heat_exhaustion, Symptoms, T) :-
    treatment_text(heat_exhaustion, T),
    member(fever, Symptoms),
    member(headache, Symptoms),
    member(nausea, Symptoms),
    member(fatigue, Symptoms).

overlap_count(UserSymptoms, Signature, N) :-
    findall(S, (member(S, Signature), member(S, UserSymptoms)), Hits),
    length(Hits, N).

ranked_candidates(UserSymptoms, Rows) :-
    findall([Score, Disease, Treatment], (
        disease_signature(Disease, Sig),
        treatment_text(Disease, Treatment),
        overlap_count(UserSymptoms, Sig, Score),
        Score >= 1
    ), Rows).

row_to_diagnosis([_, Disease, Treatment], [Disease, Treatment]).

possible_diagnoses(Symptoms, Diagnoses) :-
    findall([Disease, Treatment], diagnose(Disease, Symptoms, Treatment), Exact),
    ( Exact \= [] ->
        Diagnoses = Exact
    ;
        ranked_candidates(Symptoms, Rows),
        ( Rows = [] ->
            Diagnoses = []
        ;
            sort(Rows, SortedAsc),
            reverse(SortedAsc, Sorted),
            maplist(row_to_diagnosis, Sorted, Diagnoses)
        )
    ).

has_diagnosis(Symptoms) :-
    diagnose(_, Symptoms, _).
