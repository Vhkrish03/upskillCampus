def load_questions(filename):
    questions = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('|')
            if len(parts) == 6:
                question, option_a, option_b, option_c, option_d, correct_answer = parts
                questions.append({
                    "question": question,
                    "options": [option_a, option_b, option_c, option_d],
                    "answer": correct_answer
                })
    return questions

def quiz_game(questions):
    score = 0
    total_questions = len(questions)
    
    print("\nWelcome to the Quiz Game! Answer the questions by choosing A, B, C, or D.\n")
    
    for index, q in enumerate(questions, start=1):
        print(f"Q{index}: {q['question']}")
        for option in q['options']:
            print(option)
        
        user_answer = input("Your Answer (A/B/C/D): ").strip().upper()
        
        if user_answer == q['answer']:
            print("✅ Correct!\n")
            score += 1
        else:
            print(f"❌ Wrong! The correct answer was {q['answer']}\n")
    
    print(f"Your final score: {score}/{total_questions}")


if __name__ == "__main__":
    questions = load_questions("questions.txt")
    if questions:
        quiz_game(questions)
    else:
        print("No questions found. Please check the questions.txt file.")

