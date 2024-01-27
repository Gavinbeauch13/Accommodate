from usertb  import findUsertb


def get_review(data, school):
    reviews = data["username"]["numofreviews"]
    for review in reviews:
        if review["school"] == school:
            return float(review["review"])
        
        





{
"username": {
    "firstname": "John",
    "lastname": "Doe",
    "password": "password123",
    "numofreviews": [
      {
        "review": "4",
        "date": "2024-01-27",
        "school": "University of Washington",
        "comment": "This was a really nice school"
      },
      {
        "review": "4.5.",
        "date": "2024-01-26",
        "school": "Harvard University",
        "comment": "This was a really nice school"
      }
    ]
  }
}
