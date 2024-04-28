CLEESE's `FaceWarp` engine works by first identifying a set of landmarks on the visage present in the image. Then a gaussian distribution of
deformation vectors is applied to a subset of landmarks, and the Moving Least Squares (MLS) algorithm is used to apply the deformation to the image itself.
Alternatively, a precomputed set of deformations can also be provided.
