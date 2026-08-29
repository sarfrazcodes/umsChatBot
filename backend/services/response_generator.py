def generate_response(intent, data, query_type=None):
    if "error" in data:
        return data["error"]

    if intent == "UNKNOWN" or data.get("needs_clarification"):
        alts = data.get('alternatives', [])
        if alts:
            return f"I am not entirely sure what you mean. Did you mean something about {alts[0]} or {alts[1]}?"
        return "I'm not sure I understand. Could you please rephrase?"

    if intent == "GREETING":
        return data.get("message", "Hello Verto!")

    if intent == "ATTENDANCE":
        if "message" in data:
            return data["message"]
        overall = data.get("overall_percentage")
        return f"Your overall attendance is currently {overall}%. You have attended {data['total_attended']} out of {data['total_conducted']} classes."

    if intent == "ATTENDANCE_PROJECTION":
        if "error" in data:
            return data["error"]
            
        if data.get("is_subject_projection"):
            s_name = data["subject"]
            s_cur = data["current_subject_pct"]
            s_proj = data["projected_subject_pct"]
            s_drop = data["subject_drop"]
            o_cur = data["current_overall_pct"]
            o_proj = data["projected_overall_pct"]
            o_drop = data["overall_drop"]
            
            msg = f"If you miss that {s_name} class, your attendance in {s_name} will drop from {s_cur}% to {s_proj}% (a {s_drop}% drop), and your OVERALL attendance will drop from {o_cur}% to {o_proj}%."
            if data["warning"]:
                msg += " WARNING: This will put you below the 75% threshold!"
            return msg
        else:
            curr = data["current_percentage"]
            proj = data["projected_percentage"]
            drop = data["percentage_drop"]
            msg = f"If you miss those classes, your overall attendance will drop from {curr}% to {proj}% (a drop of {drop}%)."
            if data["warning"]:
                msg += " WARNING: This will put you below the 75% threshold!"
            return msg

    if intent == "TIMETABLE":
        if "message" in data:
            return data["message"]
        classes = data.get("classes", [])
        day = data.get("day")
        if not classes:
            return f"You have no classes scheduled for {day}."
        
        schedule_str = f"Here is your schedule for {day}:\n"
        for c in classes:
            schedule_str += f"- {c['start_time']} to {c['end_time']}: {c['subject']} (Room {c['room']})\n"
        return schedule_str

    if intent == "NEXT_CLASS":
        if "message" in data:
            return data["message"]
        nc = data["next_class"]
        return f"Your next class is {nc['subject']} at {nc['start_time']} in Room {nc['room']} with {nc['faculty']}."

    if intent == "FEES":
        if "message" in data:
            return data["message"]
        return f"Your total fee is {data['total_amount']}, out of which you have paid {data['total_paid']}. Your total pending dues are {data['total_due']}."

    if intent == "FEE_DEADLINE":
        if "message" in data:
            return data["message"]
        deadlines = data.get("deadlines", [])
        if not deadlines:
            return "You have no upcoming fee deadlines."
        d = deadlines[0]
        return f"Your closest deadline is for the {d['category']}. You have a pending amount of {d['due_amount']} due on {d['due_date']}."

    if intent == "EXAM":
        if "message" in data:
            return data["message"]
        exams = data.get("exams", [])
        if not exams:
            return "You have no upcoming exams."
        e = exams[0]
        return f"Your next exam is {e['subject_name']} on {e['date']} at {e['time']}. Venue: {e['venue']}."

    if intent == "LIBRARY":
        if "message" in data:
            return data["message"]
        books = data.get("books", [])
        if not books:
            return "No books found matching your query."
        b = books[0]
        loc = b['location']
        return f"I found '{b['title']}' by {b['author']}. It is {b['availability']} (Copies: {b['available_copies']}/{b['total_copies']}). Location: {loc['building']}, Floor {loc['floor']}, Shelf {loc['shelf']}."

    if intent == "CREATE_RMS":
        if "error" in data:
            return data["error"]
        return data["message"]

    if intent == "RMS_STATUS":
        if "message" in data:
            return data["message"]
        tickets = data.get("tickets", [])
        if not tickets:
            return "You have no open RMS tickets."
        t = tickets[0]
        return f"Your most recent ticket (#{t['ticket_id']}) regarding '{t['category']}' is currently {t['status']}."

    if intent == "HOSTEL_LEAVE":
        if "error" in data:
            return data["error"]
        return data.get("message", "Leave applied successfully.")

    if intent == "HOSTEL_LEAVE_STATUS":
        if "message" in data:
            return data["message"]
        leaves = data.get("leaves", [])
        if not leaves:
            return "You have no leave applications."
        l = leaves[0]
        return f"Your {l['type']} leave application from {l['from_date']} to {l['to_date']} is currently {l['status']}."

    if intent == "NOTICES":
        if "message" in data:
            return data["message"]
        results = data.get("results", [])
        if not results:
            return "No notices found."
        r = results[0]
        return f"Latest Notice ({r['category']}): {r['title']} - {r['content']} (Published: {r['date']})"

    if intent == "PLACEMENT_ELIGIBILITY":
        if "error" in data:
            return data["error"]
        eligible = data.get("eligible_drives", [])
        if not eligible:
            return "You are currently not eligible for any active placement drives."
        d = eligible[0]
        return f"You are eligible for the {d['company']} drive ({d['role']}). Deadline to apply: {d['deadline']}."

    if intent == "PLACEMENT_REGISTER":
        if "error" in data:
            return data["error"]
        return data.get("message", "Successfully registered for the drive.")

    if intent == "CGPA_CALCULATOR":
        if "error" in data:
            return data["error"]
            
        if data.get("is_all_subjects"):
            results = data["results"]
            if not results:
                return "No subjects found to calculate."
            
            msg = f"To achieve an {data['target_grade'].upper()} grade, here is what you need to score across your subjects:\n\n"
            for r in results:
                msg += f"**{r['subject']}**: {r['message']}\n\n"
            return msg.strip()
        else:
            return data["message"]
        
    if intent == "COURSE_INFO":
        if "error" in data:
            return data["error"]
        courses = data.get("courses", [])
        if not courses:
            return "You are not enrolled in any courses."
            
        msg = "Here are your enrolled courses and current attendance:\n"
        for c in courses:
            msg += f"- **{c['code']}**: {c['name']} | Attendance: **{c['attendance']}%**\n"
            
        return msg.strip()
    if intent == "PROFILE":
        return f"Here is your profile:\nName: {data['name']}\nRegistration: {data['registration_number']}\nBranch: {data['branch']}, Semester {data['semester']}\nCGPA: {data['cgpa']}, TGPA: {data['tgpa']}\nBacklogs: {data['backlogs']}"

    return "I processed your request but don't know how to format the response yet."
