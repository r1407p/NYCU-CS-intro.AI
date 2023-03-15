import dataset
import adaboost
import utils
import detection
import matplotlib.pyplot as plt
# Part 1: Implement loadImages function in dataset.py and test the following code.
print('Loading images')
trainData = dataset.loadImages('data/train')
print(f'The number of training samples loaded: {len(trainData)}')
testData = dataset.loadImages('data/test')
print(f'The number of test samples loaded: {len(testData)}')


print('Show the first and last images of training dataset')
"""fig, ax = plt.subplots(1, 2)
ax[0].axis('off')
ax[0].set_title('Face')
ax[0].imshow(trainData[1][0], cmap='gray')
ax[1].axis('off')
ax[1].set_title('Non face')
ax[1].imshow(trainData[-1][0], cmap='gray')
plt.show()"""


# Part 2: Implement selectBest function in adaboost.py and test the following code.
# Part 3: Modify difference values at parameter T of the Adaboost algorithm.
# And find better results. Please test value 1~10 at least.
# print('Start training your classifier')
#for training different T
"""
for t in [1,2,3,4,5,6,7,8,9,10,20,30,40,50]:
    clf = adaboost.Adaboost(T=t)
    print(f'Start training your classifier with T={t}')
    clf.train(trainData)
    clf.save(f'model/clf_200_1_{t}')
    clf = adaboost.Adaboost.load(f'model/clf_200_1_{t}')

    print('\nEvaluate your classifier with training dataset')
    utils.evaluate(clf, trainData)

    print('\nEvaluate your classifier with test dataset')
    utils.evaluate(clf, testData)
"""
t = 2
clf = adaboost.Adaboost(T=t)
print(f'Start training your classifier with T={t}')
clf.train(trainData)
#clf.save(f'model/clf_200_2_{t}')
#clf = adaboost.Adaboost.load(f'model/clf_200_2_{t}')

print('\nEvaluate your classifier with training dataset')
utils.evaluate(clf, trainData)

print('\nEvaluate your classifier with test dataset')
utils.evaluate(clf, testData)
# Part 4: Implement detect function in detection.py and test the following code.
print('\nDetect faces at the assigned location using your classifier')
detection.detect('data/detect/detectData.txt', clf)            

# Part 5: Test classifier on your own images
print('\nDetect faces on your own images')
detection.detect('data/detect/myOwnImages.txt', clf)
