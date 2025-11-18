import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# -----------------------------
# FOLDER SETUP
# -----------------------------
DATA_FOLDER = "../data"
CHART_FOLDER = "../charts"

# Create folders if not exist
os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(CHART_FOLDER, exist_ok=True)

filename = os.path.join(DATA_FOLDER, "students_marks.csv")

subjects = ["JAVA", "Python", "Machine Learning", "Data Structure", "Deep Learning"]


# -----------------------------
# GRADE CALCULATION
# -----------------------------
def calculate_grade(percentage):
    if percentage >= 90:
        return "A"
    elif percentage >= 80:
        return "B"
    elif percentage >= 70:
        return "C"
    elif percentage >= 60:
        return "D"
    else:
        return "E"


# -----------------------------
# ADD STUDENT FUNCTION
# -----------------------------
def add_student():

    student_name = input("\nEnter Student Name (or type 'exit' to finish): ")
    if student_name.lower() == "exit":
        return False

    marks = []
    print(f"\nEnter Marks for {student_name} (0-100):")

    for subject in subjects:
        while True:
            try:
                mark = float(input(f"{subject}: "))
                if 0 <= mark <= 100:
                    marks.append(mark)
                    break
                else:
                    print("Error! Enter marks between 0-100.")
            except ValueError:
                print("Invalid input, enter a number.")

    # Calculate
    total = sum(marks)
    percentage = (total / (len(subjects) * 100)) * 100
    grade = calculate_grade(percentage)

    # Prepare one row data
    data = {"Student": student_name}
    for i, subject in enumerate(subjects):
        data[subject] = marks[i]

    data["Total"] = total
    data["Percentage"] = round(percentage, 2)
    data["Grade"] = grade

    df_student = pd.DataFrame([data])

    # Save to CSV
    if os.path.exists(filename):
        df_existing = pd.read_csv(filename)
        df_final = pd.concat([df_existing, df_student], ignore_index=True)
    else:
        df_final = df_student

    df_final.to_csv(filename, index=False)
    print(f"\nData saved successfully in {filename}")

    # -----------------------------
    # SAVE BAR CHART
    # -----------------------------
    plt.figure(figsize=(8, 5))
    plt.bar(subjects, marks)
    plt.title(f"Marks of {student_name}")
    plt.xlabel("Subjects")
    plt.ylabel("Marks")
    plt.ylim(0, 100)

    for i, m in enumerate(marks):
        plt.text(i, m + 1, str(m), ha="center")

    chart_path = os.path.join(CHART_FOLDER, f"{student_name}_marks.png")
    plt.savefig(chart_path)
    plt.close()

    print(f"Chart saved successfully in {chart_path}")

    return True


# -----------------------------
# MAIN PROGRAM LOOP
# -----------------------------
print("========== STUDENT MARKS CALCULATOR ==========")

while True:
    if not add_student():
        break


# -----------------------------
# CLASS ANALYSIS
# -----------------------------
if os.path.exists(filename):
    df = pd.read_csv(filename)
    print("\n--- CLASS AVERAGE ---")
    avg = df[subjects].mean()
    print(avg)

    # Plot average bar chart
    plt.figure(figsize=(8, 5))
    plt.bar(subjects, avg)
    plt.title("Class Average Per Subject")
    plt.xlabel("Subjects")
    plt.ylabel("Average Marks")
    plt.ylim(0, 100)

    for i, a in enumerate(avg):
        plt.text(i, a + 1, str(round(a, 2)), ha="center")

    class_chart = os.path.join(CHART_FOLDER, "class_average.png")
    plt.savefig(class_chart)
    plt.close()

    print(f"\nClass average chart saved → {class_chart}")
