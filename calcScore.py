from usertb  import findUsertb


def get_review(data, school):
    review_amount = 0
    score = 0

    # reviews = data["username"]["numofreviews"]

    for users in data:
      for review in users["numofreviews"]:
          if review["school"] == school:

            review_amount += 1
            score += float(review["review"])
    
    score = (score / review_amount)
    
    return score
        
        





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
