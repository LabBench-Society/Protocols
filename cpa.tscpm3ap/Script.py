def CPMRating(tc):
   return tc.Assets.Instructions.CPRatingSuccess if tc.CPRating.RATING > 0 and tc.CPRating.RATING < 10 else tc.Assets.Instructions.CPRatingFailure