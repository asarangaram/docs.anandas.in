# CV2

## Find if a image is blurred

```python
    def is_blurred(gray):
        laplace = cv2.Laplacian(gray,3)
        var = numpy.var(laplace)
        return var < 100

    if __name__ == '__main__':
        image = cv2.imread("<file>")
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        is_blurred(gray)
```

## Find similarity between images

```python

    def similarity(im1,im2):
        img1 = cv2.imread(im1,0) 
        img2 = cv2.imread(im2,0) 

        # Initiate SIFT detector
        orb = cv2.ORB()

        # find the keypoints and descriptors with SIFT
        kp1, des1 = orb.detectAndCompute(img1,None)
        kp2, des2 = orb.detectAndCompute(img2,None)
        
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        matches = bf.match(des1,des2)

        if use_mean:
            if len(matches) is 0:
		        return 100
            lis = [m.distance for m in matches]
	        return np.mean(lis)
        else:
            if len(matches) is 0:
                return 0
            matches = sorted(matches, key=lambda x: x.distance)
            good_matches = [m for m in matches if m.distance < 0.75]
            similarity_score = len(good_matches) / len(matches)
            return similarity_score

```