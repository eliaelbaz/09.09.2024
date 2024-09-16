import sqlite3

# פונקציה להתחברות לבסיס הנתונים
def create_connection():
    connection = sqlite3.connect("hw_16.sqlite")  # מחבר לקובץ hw_16.sqlite
    return connection

# תרגיל 1: פונקציה להבאת מספר הרשומות בטבלת הזכיות
def count_winners():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM eurovision_winners")
    count = cursor.fetchone()[0]
    conn.close()
    return count

# טסט שבודק אם יש 68 רשומות בטבלת הזכיות
def test_winners_count():
    assert count_winners() == 68, f"Expected 68 winners, but got {count_winners()}"

# קריאה לטסט
test_winners_count()

# תרגיל 2: פונקציה שמחזירה את 10 הזכיות האחרונות, כולל שם השיר, ממוינות מהגדול לקטן
def get_top_10_recent_winners():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT year, song_name 
        FROM eurovision_winners 
        ORDER BY year DESC LIMIT 10
    """)
    results = cursor.fetchall()
    conn.close()
    return results

# טסט להדפסת התוצאה
def test_top_10_recent_winners():
    winners = get_top_10_recent_winners()
    for winner in winners:
        print(winner)

# קריאה לטסט
test_top_10_recent_winners()

# תרגיל 3: פונקציה שמחזירה את שם השיר הזוכה על פי מדינה ושנה
def get_winning_song(country, year):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT song_name 
        FROM eurovision_winners 
        WHERE country = ? AND year = ?
    """, (country, year))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "wrong"

# דוגמה לשימוש בפונקציה
def test_winning_song():
    print(get_winning_song("Switzerland", 2024))  # Expected: "The Code"
    print(get_winning_song("Austria", 2019))  # Expected: "wrong"

# קריאה לטסט
test_winning_song()

# תרגיל 4: טסט שבודק את הפונקציה מהתרגיל הקודם עבור מדינות ושנים שונות
def test_winning_song_various_cases():
    assert get_winning_song("Switzerland", 2024) == "The Code"
    assert get_winning_song("Austria", 2019) == "wrong"
    print("All tests passed!")

# קריאה לטסט
test_winning_song_various_cases()

# תרגיל 5: פונקציה שמשנה את הז'אנר של שיר אם הוא זכה
def update_genre(country, year, new_genre):
    if get_winning_song(country, year) != "wrong":
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE song_details 
            SET genre = ? 
            WHERE year = ? AND EXISTS (
                SELECT 1 FROM eurovision_winners 
                WHERE eurovision_winners.year = song_details.year 
                AND eurovision_winners.country = ?
            )
        """, (new_genre, year, country))
        conn.commit()
        conn.close()
        print("done")
    else:
        print("wrong")

# דוגמה לשימוש בפונקציה
def test_update_genre():
    update_genre("Switzerland", 2024, "Rock")  # Expected: done
    update_genre("Sweden", 2023, "Pop")  # Expected: enter different genre

# קריאה לטסט
test_update_genre()
