class HashtagsCreator:
  
  def __init__(self, list_of_terms):
    self.hashtags = []
    
    # Iterate through each term in the list_of_terms
    for term in list_of_terms:
      # If term contains '@', replace '@' with '#' and add to hashtags list
      if '@' in term:
        self.hashtags.append(term.replace('@', '#'))
      # If term contains '#', just add the term to hashtags list
      elif '#' in term:
        self.hashtags.append(term)
      # If neither '@' nor '#' is present in term, prepend '#' to the term and add to hashtags list
      else:
        self.hashtags.append('#' + term)
      
  def list_hashtags(self):
    # Iterate through each hashtag in self.hashtags and print it
    for hashtag in self.hashtags:
      print(hashtag)

# Testing code
test_hashtags = HashtagsCreator(["@codecademy", "#python", "programming", "#strings"])
test_hashtags.list_hashtags()
