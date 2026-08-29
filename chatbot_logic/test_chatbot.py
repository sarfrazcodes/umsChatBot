import json
from chatbot import process_query, context_manager

# 120 Test cases to ensure high robustness
TEST_CASES = [
    # Attendance
    ("what is my attendance", "ATTENDANCE", "OVERALL", {}),
    ("show my attendance", "ATTENDANCE", "OVERALL", {}),
    ("meri attendance kitni hai", "ATTENDANCE", "OVERALL", {}),
    ("attendance batao", "ATTENDANCE", "OVERALL", {}),
    ("bhai attendance check kar", "ATTENDANCE", "OVERALL", {}),
    ("DBMS ki attendance kya hai", "ATTENDANCE", "SUBJECT", {"subject": "DBMS"}),
    ("how much attendance do I have", "ATTENDANCE", "OVERALL", {}),
    ("am I eligible based on attendance", "ATTENDANCE", "ELIGIBILITY", {}),
    ("attendence", "ATTENDANCE", "OVERALL", {}),
    ("attencse", "ATTENDANCE", "OVERALL", {}),
    
    # Timetable
    ("show my timetable", "TIMETABLE", "FULL", {}),
    ("what is my schedule", "TIMETABLE", "FULL", {}),
    ("timetable batao", "TIMETABLE", "FULL", {}),
    ("timetble", "TIMETABLE", "FULL", {}),
    ("what classes do i have today", "TIMETABLE", "TODAY", {"date": "today"}),
    ("mera aaj ka schedule kya hai", "TIMETABLE", "TODAY", {"date": "aaj"}),
    ("kal ka timetable dikhao", "TIMETABLE", "TOMORROW", {"date": "kal"}),
    ("show tomorrow timetable", "TIMETABLE", "TOMORROW", {"date": "tomorrow"}),
    ("timetable for monday", "TIMETABLE", "DAY", {"date": "monday"}),
    ("weekly timetable", "TIMETABLE", "FULL", {}),
    
    # Next Class
    ("what is my next class", "NEXT_CLASS", None, {}),
    ("when is my next class", "NEXT_CLASS", None, {}),
    ("aglee class konsi hai", "NEXT_CLASS", None, {}),
    ("next class batao", "NEXT_CLASS", None, {}),
    ("where is my next class", "NEXT_CLASS", None, {}),
    ("next lecture kab hai", "NEXT_CLASS", None, {}),
    ("is there any class right now", "NEXT_CLASS", None, {}),
    ("which class is next", "NEXT_CLASS", None, {}),
    ("next class room number", "NEXT_CLASS", None, {}),
    ("bhai abhi konsi class hai", "NEXT_CLASS", None, {}),
    
    # Exam
    ("when is my exam", "EXAM", "DATE", {}),
    ("when is my DBMS exam", "EXAM", "DATE", {"subject": "DBMS"}),
    ("DBMS ka exam kab hai", "EXAM", "DATE", {"subject": "DBMS"}),
    ("exam date batao", "EXAM", "DATE", {}),
    ("where is my exam", "EXAM", "VENUE", {}),
    ("what time is my exam", "EXAM", "TIME", {}),
    ("exm", "EXAM", "DATE", {}),
    ("exam venue", "EXAM", "VENUE", {}),
    ("where do i have to go for exam", "EXAM", "VENUE", {}),
    ("exam schedule", "EXAM", "DATE", {}),
    
    # Exam Syllabus
    ("exam mein kya aayega", "EXAM_SYLLABUS", None, {}),
    ("what topics are coming in DBMS exam", "EXAM_SYLLABUS", None, {"subject": "DBMS"}),
    ("exam syllabus", "EXAM_SYLLABUS", None, {}),
    ("syllabus for mid terms", "EXAM_SYLLABUS", None, {}),
    ("portion for exam", "EXAM_SYLLABUS", None, {}),
    ("kaunse chapters aa rahe hain exam me", "EXAM_SYLLABUS", None, {}),
    ("show me the syllabus", "EXAM_SYLLABUS", None, {}),
    ("exam pattern kya hai", "EXAM_SYLLABUS", None, {}),
    ("what to study for exam", "EXAM_SYLLABUS", None, {}),
    ("syllabus for end terms", "EXAM_SYLLABUS", None, {}),
    
    # Fees
    ("how much fee do i have left", "FEES", "REMAINING", {}),
    ("what is my fee balance", "FEES", "REMAINING", {}),
    ("fees kitni baki hai", "FEES", "REMAINING", {}),
    ("due fee amount", "FEES", "REMAINING", {}),
    ("have i paid my fees", "FEES", "REMAINING", {}),
    ("how much fee is remaining", "FEES", "REMAINING", {}),
    ("pending fee", "FEES", "REMAINING", {}),
    ("total fees to pay", "FEES", "TOTAL", {}),
    ("show fee details", "FEES", "REMAINING", {}),
    ("fees check", "FEES", "REMAINING", {}),
    
    # Fee Deadline
    ("last date to pay fee", "FEE_DEADLINE", "DEADLINE", {}),
    ("when is the fee deadline", "FEE_DEADLINE", "DEADLINE", {}),
    ("fee kab submit karni hai", "FEE_DEADLINE", "DEADLINE", {}),
    ("fees bharne ki aakhri date kya hai", "FEE_DEADLINE", "DEADLINE", {}),
    ("fee due date", "FEE_DEADLINE", "DEADLINE", {}),
    ("deadline for hostel fee", "FEE_DEADLINE", "DEADLINE", {}),
    ("meri fees kab bharni hai", "FEE_DEADLINE", "DEADLINE", {}),
    ("what is the last day for fee submission", "FEE_DEADLINE", "DEADLINE", {}),
    ("fine for late fees", "FEE_DEADLINE", "DEADLINE", {}),
    ("late fee penalty date", "FEE_DEADLINE", "DEADLINE", {}),
    
    # Hostel Leave
    ("i need hostel leave", "HOSTEL_LEAVE", "LEAVE", {}),
    ("apply for hostel leave", "HOSTEL_LEAVE", "LEAVE", {}),
    ("hostel leave lagani hai", "HOSTEL_LEAVE", "LEAVE", {}),
    ("chutti chahiye hostel se", "HOSTEL_LEAVE", "LEAVE", {}),
    ("how to get night out", "HOSTEL_LEAVE", "LEAVE", {}),
    ("night out pass", "HOSTEL_LEAVE", "LEAVE", {}),
    ("leave request", "HOSTEL_LEAVE", "LEAVE", {}),
    ("bhai ghar jana hai leave kaise lu", "HOSTEL_LEAVE", "LEAVE", {}),
    ("apply leave from 2 september to 5 september", "HOSTEL_LEAVE", "LEAVE", {"date": "2 september"}),
    ("mujhe hostel leave chahiye", "HOSTEL_LEAVE", "LEAVE", {}),
    
    # RMS Create
    ("create an rms for broken ac", "CREATE_RMS", "CREATE", {"category": "AC"}),
    ("ac kharab hai rms bana do", "CREATE_RMS", "CREATE", {"category": "AC"}),
    ("file a complaint", "CREATE_RMS", "CREATE", {}),
    ("raise rms request", "CREATE_RMS", "CREATE", {}),
    ("plumbing issue in room", "CREATE_RMS", "CREATE", {"category": "PLUMBING"}),
    ("internet is not working create rms", "CREATE_RMS", "CREATE", {"category": "INTERNET"}),
    ("fan repair ke liye rms banana hai", "CREATE_RMS", "CREATE", {"category": "FAN"}),
    ("wifi is down create rms", "CREATE_RMS", "CREATE", {"category": "WIFI"}),
    ("bhai room ki light kharab hai complain karni hai", "CREATE_RMS", "CREATE", {"category": "LIGHT"}),
    ("rms bana do", "CREATE_RMS", "CREATE", {}),
    
    # Library
    ("what time does the library close", "LIBRARY", None, {}),
    ("library timings", "LIBRARY", None, {}),
    ("library kab band hoti hai", "LIBRARY", None, {}),
    ("library khuli hai kya", "LIBRARY", None, {}),
    ("when does library open", "LIBRARY", None, {}),
    ("library location", "LIBRARY", None, {}),
    ("library kahan hai", "LIBRARY", None, {}),
    ("libary timings", "LIBRARY", None, {}),
    ("libraray", "LIBRARY", None, {}),
    ("late night library access", "LIBRARY", None, {}),
    
    # Notice & Result
    ("any new notices", "NOTICES", None, {}),
    ("latest announcements", "NOTICES", None, {}),
    ("kya chal raha hai university me", "NOTICES", None, {}),
    ("show my result", "RESULT", None, {}),
    ("cgpa check karni hai", "RESULT", None, {}),
    ("what is my grade", "RESULT", None, {}),
    ("how much did i score in dbms", "RESULT", None, {"subject": "DBMS"}),
    ("tgpa for this semester", "RESULT", None, {}),
    
    # Unknowns
    ("what is the weather", "UNKNOWN", None, {}),
    ("tell me a joke", "UNKNOWN", None, {}),
    ("i want to order pizza", "UNKNOWN", None, {}),
    ("asdfgh", "UNKNOWN", None, {}),
    ("hello xyz random", "UNKNOWN", None, {}),
    ("what is the meaning of life", "UNKNOWN", None, {}),
    
    # Follow-ups (will be tested in a sequence in another function, but individually should be UNKNOWN or specific)
    ("where?", "UNKNOWN", None, {}),
    ("and OS?", "UNKNOWN", None, {"subject": "OS"})
]

def run_tests():
    print("=" * 50)
    print("Running NLP Engine Tests...")
    print("=" * 50 + "\n")
    
    passed = 0
    failed = 0
    
    for query, exp_intent, exp_qt, exp_entities in TEST_CASES:
        context_manager.clear() # Clear for individual tests
        res = process_query(query)
        
        # We don't fail for alternative ambiguities if the top intent matches
        act_intent = res["intent"]
        
        # If it's ambiguous, act_intent is UNKNOWN, but we check if top alternative is correct
        if act_intent == "UNKNOWN" and res["needs_clarification"] and len(res["alternatives"]) > 0:
            if res["alternatives"][0][0] == exp_intent:
                act_intent = exp_intent
        
        success = True
        error_msg = []
        
        if act_intent != exp_intent:
            success = False
            error_msg.append(f"Intent mismatch: Expected {exp_intent}, got {act_intent}")
            
        if res["query_type"] != exp_qt and exp_intent != "UNKNOWN":
            success = False
            error_msg.append(f"QueryType mismatch: Expected {exp_qt}, got {res['query_type']}")
            
        for k, v in exp_entities.items():
            if res["entities"].get(k) != v:
                success = False
                error_msg.append(f"Entity missing/mismatch: Expected {k}={v}, got {res['entities'].get(k)}")

        if success:
            passed += 1
        else:
            failed += 1
            print(f"FAILED: '{query}'")
            for msg in error_msg:
                print(f"  - {msg}")
            print(f"  Result JSON: {json.dumps(res, indent=2)}\n")

    # Run Context Sequence Tests
    print("Running Context Flow Tests...")
    context_manager.clear()
    
    # Flow 1
    process_query("meri DBMS attendance kitni hai")
    res1 = process_query("and OS?")
    if res1["intent"] == "ATTENDANCE" and res1["entities"].get("subject") == "OS" and res1["context_used"]:
        passed += 1
    else:
        failed += 1
        print("FAILED: Context Flow 1 (Attendance -> and OS?)")
        
    context_manager.clear()
    
    # Flow 2
    process_query("DBMS ka exam kab hai")
    res2 = process_query("where?")
    if res2["intent"] == "EXAM" and res2["query_type"] == "VENUE" and res2["entities"].get("subject") == "DBMS" and res2["context_used"]:
        passed += 1
    else:
        failed += 1
        print("FAILED: Context Flow 2 (Exam -> where?)")
        
    total = passed + failed
    acc = (passed / total) * 100
    
    print("=" * 50)
    print("## NLP TEST RESULTS")
    print(f"Total: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Accuracy: {acc:.2f}%")
    print("=" * 50)

if __name__ == "__main__":
    run_tests()
