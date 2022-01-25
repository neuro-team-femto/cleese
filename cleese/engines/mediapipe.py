#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image
import mediapipe as mp
from os import path

from .engine import Engine
from cleese.third_party.mls.img_utils import mls_rigid_deformation


class Mediapipe(Engine):

    @staticmethod
    def load_file(filename):
        return np.array(Image.open(filename)), {}

    @staticmethod
    def process(image, config, file_output=False, **kwargs):
        # FIXME Replace with config values
        lips_idx = [61, 40, 37, 0, 267, 270, 291, 321, 314, 17, 84, 181, 91,
                    78, 80, 13, 311, 308, 402, 14, 178]
        mls_idx = [61, 40, 78, 91, 270, 308, 321, 291]

        # TODO Apply dfm to image
        height, width, _ = image.shape
        target_img = image.copy()

        p = []
        q = []

        with mp.solutions.face_mesh.FaceMesh(
                static_image_mode=True,
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5) as face_mesh:

            results = face_mesh.process(image)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:

                    selected_con = mp.solutions.face_mesh.FACEMESH_CONTOURS
                    mp.solutions.drawing_utils.draw_landmarks(
                            image=target_img,
                            landmark_list=face_landmarks,
                            connections=selected_con,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=mp.solutions.drawing_styles
                            .get_default_face_mesh_contours_style())

                    # Get points for the MLS
                    for i in lips_idx:
                        lm = face_landmarks.landmark[i]
                        x = int(lm.x * width)
                        y = int(lm.y * height)
                        p.append([x, y])
                        if i in mls_idx:
                            q.append([x, y + abs(x - 230) * 0.5 - 5])
                        else:
                            q.append([x, y])

        # Setup fixed anchor point on the image's corners for the MLS
        p.append([0, 0])
        q.append([0, 0])
        p.append([width - 1, 0])
        q.append([width - 1, 0])
        p.append([width - 1, height - 1])
        q.append([width - 1, height - 1])
        p.append([0, height - 1])
        q.append([0, height - 1])

        p = np.array(p)
        q = np.array(q)

        gridX = np.arange(0, width, dtype=np.int16)
        gridY = np.arange(0, height, dtype=np.int16)
        vy, vx = np.meshgrid(gridX, gridY)

        # mls_rigid_deformation expects coordinates in the (y, x) order
        p_mls = p[:, [1, 0]]
        q_mls = q[:, [1, 0]]
        rigid = mls_rigid_deformation(vy, vx, p_mls, q_mls, alpha=1.2)
        aug3 = np.ones_like(image)
        aug3[vx, vy] = image[tuple(rigid)]

        return aug3

    @staticmethod
    def generate_stimuli(img, config, **kwargs):
        # FIXME Replace with config values
        lips_idx = [61, 40, 37, 0, 267, 270, 291, 321, 314, 17, 84, 181, 91,
                    78, 80, 13, 311, 308, 402, 14, 178]

        # Check all the needed user-provided config values are here
        try:
            MLS_ALPHA = config["mediapipe"]["mls"]["alpha"]
            COVARIANCE_MAT = config["mediapipe"]["random_gen"]["covMat"]
            LANDMARKS_TYPES = config["mediapipe"]["random_gen"]["landmarks"]
            NUM_FILES = config["main"]["numFiles"]
            FACE_THRESH = config["mediapipe"]["face_detect"]["threshold"]
        except KeyError as e:
            print("ERROR: missing config element: {}".format(e))
            return

        # Internal values, should never be missing
        BASE_DIR = config["main"]["expBaseDir"]
        FILENAME = config["main"]["filename"]

        height, width, _ = img.shape

        p = []
        mls_targets = []
        for key in LANDMARKS_TYPES:
            if key == "mediapipe":
                mls_targets += LANDMARKS_TYPES[key]
            elif key == "dlib":
                print("WARN: dlib indices not yet implemented")
            elif key == "presets":
                print("WARN: landmarks presets not yet implemented")
            else:
                print("ERROR: unknown landmark indexing: {}".format(key))

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
            print("ERROR: unable to detect any faces")
            return

        np_landmarks = []
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

        # Export landmark positions to file
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
            print("Random face deformation [mediapipe]: {}/{}"
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
                    basename[0], i + 1, ".dfmxy"))
            dfmxy = np.hstack((np.array([mls_targets]).T, p[:-4], mls_offsets))
            np.savetxt(output_dfm_file,
                       dfmxy,
                       fmt="%d,%d,%d,%.8f,%.8f",
                       header="mediapipe idx, posX, posY, defX, defY")

    @staticmethod
    def name():
        return "mediapipe"
