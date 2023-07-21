import cv2
import numpy as np
from statistics import mean
from numpy import ones, vstack
from numpy.linalg import lstsq


def get_slope(line):
    slope = None
    try:
        x = line[0] - line[2]
        y = line[1] - line[3]

        slope = np.divide(y, x)
    except ZeroDivisionError:
        slope = None
    finally:
        return slope


def average_lane(lane_data):
    x1s = []
    y1s = []
    x2s = []
    y2s = []
    for data in lane_data:
        x1s.append(data[2][0])
        y1s.append(data[2][1])
        x2s.append(data[2][2])
        y2s.append(data[2][3])
    return int(mean(x1s)), int(mean(y1s)), int(mean(x2s)), int(mean(y2s))


def draw_lanes_simple(img, lines, color=[0, 255, 255], thickness=3):
    try:
        for coords in lines:
            coords = np.array(coords, dtype='uint32')
            cv2.line(img,
                     (coords[0], coords[1]),
                     (coords[2], coords[3]),
                     color=color, thickness=thickness)
            cv2.line(img,
                     (coords[0] * 5, coords[1] * 5),
                     (coords[2] * 5, coords[3] * 5),
                     color=[0, 255, 0], thickness=thickness)

    except Exception as e:
        print('draw lines error : {}'.format(e))


def draw_lanes(img, lines, color=[0, 255, 255], thickness=3):
    # if this fails, go with some default line
    try:
        ys = []
        for i in lines:
            for ii in i:
                ys += [ii[1], ii[3]]
        min_y = min(ys)
        max_y = 1024
        new_lines = []
        line_dict = {}

        for idx, i in enumerate(lines):
            for xyxy in i:
                # from http://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points
                # Used to calculate the definition of a line, given two sets of coords.
                x_coords = (xyxy[0], xyxy[2])
                y_coords = (xyxy[1], xyxy[3])
                A = vstack([x_coords, ones(len(x_coords))]).T
                m, b = lstsq(A, y_coords, rcond=None)[0]

                # Calculating our new, and improved, xs
                x1 = (min_y - b) / m
                x2 = (max_y - b) / m

                line_dict[idx] = [m, b, [int(x1), min_y, int(x2), max_y]]
                new_lines.append([int(x1), min_y, int(x2), max_y])

        final_lanes = {}

        for idx in line_dict:
            final_lanes_copy = final_lanes.copy()
            m = line_dict[idx][0]
            b = line_dict[idx][1]
            line = line_dict[idx][2]

            if len(final_lanes) == 0:
                final_lanes[m] = [[m, b, line]]

            else:
                found_copy = False

                for other_ms in final_lanes_copy:

                    if not found_copy:
                        if abs(other_ms * 1.2) > abs(m) > abs(other_ms * 0.8):
                            if abs(final_lanes_copy[other_ms][0][1] * 1.2) > abs(b) > abs(
                                    final_lanes_copy[other_ms][0][1] * 0.8):
                                final_lanes[other_ms].append([m, b, line])
                                found_copy = True
                                break
                        else:
                            final_lanes[m] = [[m, b, line]]

        line_counter = {}

        for lanes in final_lanes:
            line_counter[lanes] = len(final_lanes[lanes])

        top_lanes = sorted(line_counter.items(), key=lambda item: item[1])[::-1][:2]

        lane1_id = top_lanes[0][0]
        lane2_id = top_lanes[1][0]

        l1_x1, l1_y1, l1_x2, l1_y2 = average_lane(final_lanes[lane1_id])
        l2_x1, l2_y1, l2_x2, l2_y2 = average_lane(final_lanes[lane2_id])

        return [l1_x1, l1_y1, l1_x2, l1_y2], [l2_x1, l2_y1, l2_x2, l2_y2], lane1_id, lane2_id
    except Exception as e:
        print(str(e))


def getLines(image):
    """Deprecated"""
    lines = cv2.HoughLinesP(image, 0.3, np.pi / 180, 100, np.array([]), minLineLength=70, maxLineGap=20)
    return lines


def displayLines(image, lines):
    """Deprecated"""
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)  # converting to 1d array
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return image


def getLineCoordinatesFromParameters(image, line_parameters):
    """Deprecated"""
    slope = line_parameters[0]
    intercept = line_parameters[1]
    y1 = image.shape[0]
    y2 = int(y1 * (3.4 / 5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])


def getSmoothLines(image, lines):
    """Deprecated"""
    left_fit = []
    right_fit = []

    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)

    left_line = getLineCoordinatesFromParameters(image, left_fit_average)
    right_line = getLineCoordinatesFromParameters(image, right_fit_average)
    return np.array([left_line, right_line])
