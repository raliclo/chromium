// Copyright 2026 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

package org.chromium.base;

import android.os.Build;

/**
 * Android releases older than this build's minimum (Lollipop, API 21) on which the compat paths run.
 *
 * Chromium 88 calls API 21 classes and methods directly. On an older device that has one of the levels
 * listed here, the few places that would throw (NoClassDefFoundError, NoSuchMethodError) take a
 * pre-Lollipop path instead. Everywhere else, and on every level not listed, the code is unchanged.
 * The embedder chooses the levels with {@link #setLevels} before Chromium starts; the default is
 * KitKat (19) and KitKat watch (20).
 */
public final class LegacySdk {
    private static volatile int[] sLevels = {Build.VERSION_CODES.KITKAT, Build.VERSION_CODES.KITKAT_WATCH};

    private LegacySdk() {}

    /** Sets the API levels below 21 that get the compat paths; none turns them all off. */
    public static void setLevels(int... levels) {
        sLevels = levels == null ? new int[0] : levels.clone();
    }

    /** The API levels that get the compat paths. */
    public static int[] getLevels() {
        return sLevels.clone();
    }

    /** Whether this device runs one of the chosen levels, all of which are below Lollipop. */
    public static boolean isActive() {
        int sdk = Build.VERSION.SDK_INT;
        if (sdk >= Build.VERSION_CODES.LOLLIPOP) return false;
        for (int level : sLevels) {
            if (level == sdk) return true;
        }
        return false;
    }
}
