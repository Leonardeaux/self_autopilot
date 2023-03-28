import cv2
import numpy as np
import lines_managing as lm
import utils

from sklearn.cluster import KMeans


def roi(img, vertices):
    mask = np.zeros_like(img)

    cv2.fillPoly(mask, vertices, 255)

    masked = cv2.bitwise_and(img, mask)

    return masked


def process_img(image):
    original_image = image

    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)

    processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0)

    processed_img = roi(processed_img, [utils.VERTICES_FIRST_PERSON])

    return processed_img, original_image


def process_img_avg_lines(image):
    processed_img, original_image = process_img(image)

    lines = cv2.HoughLinesP(processed_img, 1, np.pi / 180, 180, 120, 20)

    try:
        l1, l2 = lm.draw_lanes(original_image, lines)
        cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), [255, 0, 0], 15)
        cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), [255, 0, 0], 15)
    except Exception as e:
        print(str(e))
        pass
    # try:
    #     for coords in lines:
    #         coords = coords[0]
    #         try:
    #             cv2.line(processed_img, (coords[0], coords[1]), (coords[2], coords[3]), [255, 0, 0], 3)
    #
    #         except Exception as e:
    #             print(str(e))
    # except Exception as e:
    #     pass

    return processed_img, original_image


def process_image_kmeans(image):
    processed_img, original_image = process_img(image)

    lines = cv2.HoughLinesP(processed_img, 1, np.pi / 180, 180, 120, 20)

    try:
        nlines = np.array([l[0] for l in lines])
        kmeans = KMeans(n_clusters=2, random_state=0, n_init='auto').fit(nlines)
        lm.draw_lanes_simple(original_image, kmeans.cluster_centers_)
    except (ValueError, TypeError) as e:
        print('KMeans error: {}'.format(e))

    return processed_img, original_image
