# Root Cause Analysis (RCA) Report Template

## 1. Incident Summary

- Incident ID
- Timestamp
- Automation Platform
- Process Name
- Automation Agent / Robot
- Workflow Name
- Failed Activity
- Exception
- Incident Category
- Incident Subcategory
- Severity

---

## 2. Incident Description

A concise summary describing the automation failure and its observed impact.

---

## 3. Failure Location

- Workflow
- Parent Workflow
- Activity
- Sequence / Flowchart
- Inside Loop? (Yes/No)
- Inside Conditional Branch? (Yes/No)
- Application
- Screen / Page
- URL (if applicable)

---

## 4. Execution Context

- Previous Log Entries
- Failed Log Entry
- Subsequent Log Entry (if available)
- Relevant Input Parameters
- Environment Information (if available)

---

## 5. Similar Historical Incidents

- Similar Incident IDs
- Previous Resolution
- Number of Previous Occurrences

---

## 6. Probable Root Causes

Ranked list of the most probable root causes with confidence scores.

---

## 7. Supporting Evidence

Evidence retrieved from execution logs, incident history, and runtime context supporting the diagnosis.

---

## 8. Recommended Recovery Actions

Ordered list of recommended recovery actions based on retrieved knowledge and AI reasoning.

---

## 9. Platform-Specific Recommendations *(Optional)*

When applicable, recommend automation-platform-specific solutions.

**Example (UiPath):**

- Retry Scope
- Check App State
- Element Exists
- Use Application/Browser
- Wait for Ready

Future implementations may include recommendations for other enterprise automation platforms.

---

## 10. Estimated Recovery Time

Estimated effort required to resolve the incident.

---

## 11. Prevention Recommendations

Recommendations to reduce the likelihood of similar incidents occurring in the future.

---

## 12. References

Relevant documentation, knowledge-base articles, historical incidents, or vendor documentation referenced during diagnosis.

---

## 13. Confidence Score

Overall confidence score of the generated diagnosis and recommendations.