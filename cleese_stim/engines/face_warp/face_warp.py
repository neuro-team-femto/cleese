#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
CLEESE toolbox v2.0
jan 2022, Lara Kermarec <lara.git@kermarec.bzh> for CNRS

Image deformation engine for CLEESE, using mediapipe
'''

import numpy as np
from numpy.lib import recfunctions as rfn
from PIL import Image
import mediapipe as mp
from os import path
from scipy.spatial import Delaunay

from ..engine import Engine
from ...cleese import log
from ...third_party.mls.img_utils import mls_rigid_deformation


DLIB_TO_MEDIAPIPE = [
        162, 254, 132, 58, 172, 136, 150, 176,  # Face oval right
        152,  # Chin
        400, 379, 365, 397, 288, 361, 454, 389,  # Face oval left
        70, 63, 105, 66, 107,  # Eyebrow top right
        336, 296, 334, 293, 300,  # Eyebrow top left
        168, 187, 5, 1, 98, 97, 2, 326, 327,  # Nose
        33, 160, 158, 133, 153, 144,  # Eye right
        362, 385, 387, 263, 373, 380,  # Eye left
        61, 40, 37, 0, 267, 270, 291, 321, 314, 17, 84, 91,  # Outer lips
        78, 80, 13, 311, 308, 402, 14, 178,  # Inner lips
]

LANDMARKS_SETS = {
        "dlib-eyebrow-right": DLIB_TO_MEDIAPIPE[17:22],
        "dlib-eyebrow-left": DLIB_TO_MEDIAPIPE[22:27],
        "dlib-nose": DLIB_TO_MEDIAPIPE[27:36],
        "dlib-eye-right": DLIB_TO_MEDIAPIPE[36:42],
        "dlib-eye-left": DLIB_TO_MEDIAPIPE[42:48],
        "dlib-outer-lips": DLIB_TO_MEDIAPIPE[48:60],
        "dlib-inner-lips": DLIB_TO_MEDIAPIPE[60:68],
        "dlib-lips": DLIB_TO_MEDIAPIPE[48:68],
        "dlib-all": DLIB_TO_MEDIAPIPE[17:68],
        "mediapipe-all": list(np.arange(468))
}

MEDIAPIPE_TO_DLIB = [
        51,  # [0]
        30,  # [1]
        33,  # [2]
        -1, -1,
        29,  # [5]
        -1, -1, -1, -1, -1, -1, -1,
        62,  # [13]
        66,  # [14]
        -1, -1,
        57,  # [17]
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        36,  # [33]
        -1, -1, -1,
        50,  # [37]
        -1, -1,
        49,  # [40]
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        3,  # [58]
        -1, -1,
        48,  # [61]
        -1,
        18,  # [63]
        -1, -1,
        20,  # [66]
        -1, -1, -1,
        17,  # [70]
        -1, -1, -1, -1, -1, -1, -1,
        60,  # [78]
        -1,
        61,  # [80]
        -1, -1, -1,
        58,  # [84]
        -1, -1, -1, -1, -1, -1,
        59,  # [91]
        -1, -1, -1, -1, -1,
        32,  # [97]
        31,  # [98]
        -1, -1, -1, -1, -1, -1,
        19,  # [105]
        -1,
        21,  # [107]
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        2,  # [132]
        39,  # [133]
        -1, -1,
        5,  # [136]
        -1, -1, -1, -1, -1, -1, -1,
        41,  # [144]
        -1, -1, -1, -1, -1,
        6,  # [150]
        -1,
        8,  # [152]
        40,  # [153]
        -1, -1, -1, -1,
        38,  # [158]
        -1,
        37,  # [160]
        -1,
        0,  # [162]
        -1, -1, -1, -1, -1,
        27,  # [168]
        -1, -1, -1,
        4,  # [172]
        -1, -1, -1,
        7,  # [176]
        -1,
        67,  # [178]
        -1, -1, -1, -1, -1, -1, -1, -1,
        28,  # [187]
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        1,  # [254]
        -1, -1, -1, -1, -1, -1, -1, -1,
        45,  # [263]
        -1, -1, -1,
        52,  # [267]
        -1, -1,
        53,  # [270]
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        13,  # [288]
        -1, -1,
        54,  # [291]
        -1,
        25,  # [293]
        -1, -1,
        23,  # [296]
        -1, -1, -1,
        26,  # [300]
        -1, -1, -1, -1, -1, -1, -1,
        64,  # [308]
        -1, -1,
        63,  # [311]
        -1, -1,
        56,  # [314]
        -1, -1, -1, -1, -1, -1,
        55,  # [321]
        -1, -1, -1, -1,
        34,  # [326]
        35,  # [327]
        -1, -1, -1, -1, -1, -1,
        24,  # [334]
        -1,
        22,  # [336]
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1,
        14,  # [361]
        42,  # [362]
        -1, -1,
        11,  # [365]
        -1, -1, -1, -1, -1, -1, -1,
        46,  # [373]
        -1, -1, -1, -1, -1,
        10,  # [379]
        47,  # [380]
        -1, -1, -1, -1,
        43,  # [385]
        -1,
        44,  # [387]
        -1,
        16,  # [389]
        -1, -1, -1, -1, -1, -1, -1,
        12,  # [397]
        -1, -1,
        9,  # [400]
        -1,
        65,  # [402]
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        15,  # [454]
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
]


def dlib_to_mediapipe(dlib_landmarks):
    return np.take(DLIB_TO_MEDIAPIPE, dlib_landmarks, axis=0)


def mediapipe_to_dlib(mediapipe_landmarks):
    dlib = np.take(MEDIAPIPE_TO_DLIB, mediapipe_landmarks, axis=0)
    if -1 in dlib:
        raise IndexError()
    return dlib


class FaceWarp(Engine):

    @staticmethod
    def load_file(filename):
        return np.array(Image.open(filename).convert("RGB")), {}

    @staticmethod
    def load_dfm(filename):
        dfm = None
        try:
            dfm = np.genfromtxt(filename,
                                dtype=[
                                    ("group", "i4"),
                                    ("index", "i4"),
                                    ("v1", "i4"),
                                    ("v2", "i4"),
                                    ("v3", "i4"),
                                    ("alpha", "f8"),
                                    ("beta", "f8"),
                                    ("gamma", "f8"),
                                ],
                                delimiter=",",
                                invalid_raise=True)
        except ValueError:
            log("ERROR: invalid dfm file: {}".format(filename))
        except OSError as e:
            log("ERROR: {}".format(e))
        return dfm

    @staticmethod
    def load_dfmxy(filename):
        dfm = None
        try:
            dfm = np.genfromtxt(filename,
                                dtype=[
                                    ("index", "i4"),
                                    ("posX", "i4"),
                                    ("posY", "i4"),
                                    ("defX", "f8"),
                                    ("defY", "f8"),
                                ],
                                delimiter=",",
                                invalid_raise=True)
        except ValueError:
            log("ERROR: invalid dfm file: {}".format(filename))
        except OSError as e:
            log("ERROR: {}".format(e))
        return dfm

    @staticmethod
    def load_landmarks(filename):
        lm = None
        try:
            lm = np.loadtxt(filename)
            if lm.ndim != 2 or lm.shape[1] != 2:
                log(("ERROR: {}, expected landmarks file with shape (N, 2), "
                     "got {}").format(filename, lm.shape))
                return None
        except OSError as e:
            log("ERROR: {}".format(e))
        return lm

    @staticmethod
    def process(img, config, file_output=False, dfm=None, dfmxy=None):

        # Check all the needed user-provided config values are here
        try:
            MLS_ALPHA = config["mediapipe"]["mls"]["alpha"]
            COVARIANCE_MAT = config["mediapipe"]["random_gen"]["covMat"]
            LANDMARKS_TYPES = config["mediapipe"]["random_gen"]["landmarks"]
            # NUM_FILES = config["main"]["numFiles"]
            FACE_THRESH = config["mediapipe"]["face_detect"]["threshold"]
        except KeyError as e:
            log("ERROR: missing config element: {}".format(e))
            return

        if dfm is not None and dfmxy is not None:
            log("WARN: non empty dfm and dfmxy provided. Ignoring dfmxy")

        mls_targets = []
        if dfm is not None:
            mls_targets += dlib_to_mediapipe(dfm["index"]).tolist()
            triangles_indices = dlib_to_mediapipe(
                    rfn.structured_to_unstructured(
                        dfm[["v1", "v2", "v3"]]))
        elif dfmxy is not None:
            mls_targets += dfmxy["index"].tolist()
        else:
            for key in LANDMARKS_TYPES:
                if key == "mediapipe":
                    mls_targets += LANDMARKS_TYPES[key]
                elif key == "dlib":
                    try:
                        mls_targets += dlib_to_mediapipe(
                                LANDMARKS_TYPES[key]).tolist()
                    except IndexError:
                        log("WARN: dlib landmark index outside of [0, 67]")
                elif key == "presets":
                    for preset in LANDMARKS_TYPES[key]:
                        if preset in LANDMARKS_SETS:
                            mls_targets += LANDMARKS_SETS[preset]
                        else:
                            log("WARN: unknown landmark preset: {}".format(
                                    preset))
                else:
                    log("ERROR: unknown landmark indexing: {}".format(key))

        # Retrieve face landmarks from Mediapipe
        results = None
        with mp.solutions.face_mesh.FaceMesh(
                static_image_mode=True,
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=FACE_THRESH) as face_mesh:

            results = face_mesh.process(img)

        # Get points for the MLS
        if not results or not results.multi_face_landmarks:
            log("ERROR: unable to detect any faces")
            return

        rng = np.random.default_rng()

        # Retrieve targeted landmarks for Mediapipe's results
        height, width, _ = img.shape
        for face_landmarks in results.multi_face_landmarks:
            # Compute pixel size of the detected face
            x = [int(lm.x * width) for lm in face_landmarks.landmark]
            y = [int(lm.y * height) for lm in face_landmarks.landmark]
            np_landmarks = np.column_stack((x, y))
            face_min = np.amin(np_landmarks, axis=0)
            face_max = np.amax(np_landmarks, axis=0)
            face_size = face_max[1] - face_min[1]

            # Select landmarks to be deformed
            p = np.take(np_landmarks, np.array(mls_targets), axis=0)

            if dfm is not None:
                # Apply barycentric coordinates to get target points
                t = np.take(np_landmarks, triangles_indices, axis=0)
                weights = rfn.structured_to_unstructured(
                        dfm[["alpha", "beta", "gamma"]])
                q = np.sum(t * weights[:, :, np.newaxis], axis=1)
                q = q.astype(np.int16)
            elif dfmxy is not None:
                mls_offsets = rfn.structured_to_unstructured(
                        dfmxy[["defX", "defY"]])
                q = p + mls_offsets
            else:
                # Compute gaussian-distributed offsets
                mls_offsets = rng.multivariate_normal((0, 0),
                                                      COVARIANCE_MAT,
                                                      len(mls_targets))
                mls_offsets *= face_size
                q = p + mls_offsets

        # Setup fixed anchor point on the image's corners for the MLS
        box = np.array([
            (0, 0),
            (width - 1, 0),
            (width - 1, height - 1),
            (0, height - 1),
        ])
        p = np.concatenate((p, box))
        q = np.concatenate((q, box))

        gridX = np.arange(0, width, dtype=np.int16)
        gridY = np.arange(0, height, dtype=np.int16)
        vy, vx = np.meshgrid(gridX, gridY)

        # mls_rigid_deformation expects coordinates in the (y, x) order
        p_mls = p[:, [1, 0]]
        q_mls = q[:, [1, 0]]
        rigid = mls_rigid_deformation(vy, vx,
                                      p_mls, q_mls,
                                      alpha=MLS_ALPHA)

        # Apply the computed deformation to the image
        deformed_img = np.ones_like(img)
        deformed_img[vx, vy] = img[tuple(rigid)]

        return deformed_img

    @staticmethod
    def generate_stimuli(img, config, **kwargs):

        # default configuration values
        try:
            DFMXY_EXT = config["main"]["param_ext"]
        except KeyError as e:
            DFMXY_EXT = '.txt' # default dfm extension is .txt

        # Check all the needed user-provided config values are here
        try:
            MLS_ALPHA = config["mediapipe"]["mls"]["alpha"]
            COVARIANCE_MAT = config["mediapipe"]["random_gen"]["covMat"]
            LANDMARKS_TYPES = config["mediapipe"]["random_gen"]["landmarks"]
            NUM_FILES = config["main"]["numFiles"]
            FACE_THRESH = config["mediapipe"]["face_detect"]["threshold"]
        except KeyError as e:
            log("ERROR: missing config element: {}".format(e))
            return

        # Internal values, should never be missing
        BASE_DIR = config["main"]["expBaseDir"]
        FILENAME = config["main"]["filename"]

        # Load all the different sources of landmark targets
        mls_targets = []
        for key in LANDMARKS_TYPES:
            if key == "mediapipe":
                mls_targets += LANDMARKS_TYPES[key]
            elif key == "dlib":
                try:
                    mls_targets += dlib_to_mediapipe(
                            LANDMARKS_TYPES[key]).tolist()
                except IndexError:
                    log("WARN: dlib landmark index outside of [0, 67]")
            elif key == "presets":
                for preset in LANDMARKS_TYPES[key]:
                    if preset in LANDMARKS_SETS:
                        mls_targets += LANDMARKS_SETS[preset]
                    else:
                        log("WARN: unknown landmark preset: {}".format(preset))
            else:
                log("ERROR: unknown landmark indexing: {}".format(key))

        rng = np.random.default_rng()

        # Retrieve face landmarks from Mediapipe
        results = None
        with mp.solutions.face_mesh.FaceMesh(
                static_image_mode=True,
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=FACE_THRESH) as face_mesh:

            results = face_mesh.process(img)

        # Get points for the MLS
        if not results or not results.multi_face_landmarks:
            log("ERROR: unable to detect any faces")
            return

        # Retrieve targeted landmarks for Mediapipe's results
        height, width, _ = img.shape
        np_landmarks = []
        p = []
        for face_landmarks in results.multi_face_landmarks:
            # Compute pixel size of the detected face
            x = [int(lm.x * width) for lm in face_landmarks.landmark]
            y = [int(lm.y * height) for lm in face_landmarks.landmark]
            np_landmarks = np.column_stack((x, y))
            face_min = np.amin(np_landmarks, axis=0)
            face_max = np.amax(np_landmarks, axis=0)
            face_size = face_max[1] - face_min[1]

            # Select landmarks to be deformed
            for i, lm_idx in enumerate(mls_targets):
                pt = np_landmarks[lm_idx]
                p.append(pt)

        # Export landmarks positions to file
        basename = path.splitext(path.basename(FILENAME))
        output_landmarks_file = path.join(
                BASE_DIR, "{}.landmarks.txt".format(basename[0]))
        np.savetxt(output_landmarks_file,
                   np_landmarks,
                   fmt="%d",
                   header="landmarks X, Y")

        # Setup fixed anchor point on the image's corners for the MLS
        p.append([0, 0])
        p.append([width - 1, 0])
        p.append([width - 1, height - 1])
        p.append([0, height - 1])
        p = np.array(p)

        gridX = np.arange(0, width, dtype=np.int16)
        gridY = np.arange(0, height, dtype=np.int16)
        vy, vx = np.meshgrid(gridX, gridY)

        for i in range(NUM_FILES):
            log("Random face deformation [facewarp]: {}/{}"
                .format(i + 1, NUM_FILES))

            # Compute gaussian-distributed offsets
            mls_offsets = rng.multivariate_normal((0, 0),
                                                  COVARIANCE_MAT,
                                                  len(mls_targets))
            mls_offsets *= face_size
            q = p[:-4] + mls_offsets
            q = np.concatenate((q, p[-4:]))

            # mls_rigid_deformation expects coordinates in the (y, x) order
            p_mls = p[:, [1, 0]]
            q_mls = q[:, [1, 0]]
            rigid = mls_rigid_deformation(vy, vx,
                                          p_mls, q_mls,
                                          alpha=MLS_ALPHA)

            # Apply the computed deformation to the image
            deformed_img = np.ones_like(img)
            deformed_img[vx, vy] = img[tuple(rigid)]

            # Export deformed image to file
            output_img_file = path.join(BASE_DIR, "{}.{:08d}{}".format(
                    basename[0], i + 1, basename[1]))
            out_image = Image.fromarray(deformed_img)
            out_image.save(output_img_file)

            # Export deformed landmarks to file
            output_dfm_file = path.join(BASE_DIR, "{}.{:08d}{}".format(
                    basename[0], i + 1, DFMXY_EXT))
            dfmxy = np.hstack((np.array([mls_targets]).T, p[:-4], mls_offsets))
            np.savetxt(output_dfm_file,
                       dfmxy,
                       fmt="%d,%d,%d,%.8f,%.8f",
                       header="idx, posX, posY, defX, defY", 
                       comments="")

    @staticmethod
    def dfmxy_to_dfm(dfmxy_file, landmarks_file, output_dfm_file=None):
        dfmxy = FaceWarp.load_dfmxy(dfmxy_file)
        if dfmxy is None:
            return

        landmarks = FaceWarp.load_landmarks(landmarks_file)
        if landmarks is None:
            return

        if output_dfm_file is None:
            output_dfm_file = path.splitext(dfmxy_file)[0] + ".dfm"

        dfmxy_pts = rfn.structured_to_unstructured(dfmxy[["posX", "posY"]])
        dfmxy_def = rfn.structured_to_unstructured(dfmxy[["defX", "defY"]])
        targets = dfmxy_pts + dfmxy_def

        try:
            dlib_idx = mediapipe_to_dlib(dfmxy["index"])
        except IndexError:
            log(("ERROR: dfmxy has indices without dlib counterparts. "
                 "Cannot convert."))
            return

        dlib_landmarks = np.take(landmarks, DLIB_TO_MEDIAPIPE, axis=0)
        tri = Delaunay(dlib_landmarks)
        target_triangles = tri.find_simplex(targets, bruteforce=True, tol=0.01)

        dfm = np.empty((len(dlib_idx), 8))
        trans_targets = targets - tri.transform[target_triangles, 2]
        for i, t in enumerate(target_triangles):
            b = tri.transform[t, :2].dot(np.transpose(trans_targets[i]))
            # group all landmarks in group 0
            # better than trying to guess at group composition
            dfm[i] = np.concatenate(([0, dlib_idx[i]],
                                     tri.simplices[t],
                                     np.transpose(b),
                                     [1 - b.sum(axis=0)]))

        np.savetxt(output_dfm_file,
                   dfm,
                   fmt="%d,%d,%d,%d,%d,%.8f,%.8f,%.8f",
                   header=("group, index, triangle indices {0, 1, 2}, "
                           "barycentric coords weights {alpha, beta, gamma}"))

    @staticmethod
    def name():
        return "facewarp"

    @staticmethod
    def img_read(file_name): 
        return FaceWarp.load_file(file_name)[0]

    @staticmethod
    def img_write(img_array, file_name): 
        img = Image.fromarray(img_array)
        img.save(file_name)


