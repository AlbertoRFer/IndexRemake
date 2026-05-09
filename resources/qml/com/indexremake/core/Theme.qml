pragma Singleton
import QtQuick

QtObject {
    id: root

    // --- Surfaces (dark mode defaults) ---
    readonly property color surface0: "#141416"
    readonly property color surface1: "#1C1C1F"
    readonly property color surface2: "#252528"
    readonly property color surface3: "#2E2E32"

    // --- Text ---
    readonly property color textPrimary: "#E8E8EA"
    readonly property color textSecondary: Qt.rgba(0.91, 0.91, 0.92, 0.70)
    readonly property color textTertiary: Qt.rgba(0.91, 0.91, 0.92, 0.40)

    // --- Accent ---
    readonly property color accent: "#4A9EFF"
    readonly property color accentSubtle: Qt.rgba(0.29, 0.62, 1.0, 0.12)

    // --- Borders ---
    readonly property color borderSubtle: Qt.rgba(1, 1, 1, 0.06)
    readonly property color borderMid: Qt.rgba(1, 1, 1, 0.10)

    // --- Semantic (for future use) ---
    readonly property color success: "#1EB464"
    readonly property color warning: "#C88C1E"
    readonly property color danger: "#E05252"

    // --- Typography ---
    readonly property string fontFamily: "Inter"

    readonly property int textSizeMeta: 13
    readonly property int textSizeLabel: 14
    readonly property int textSizeBody: 15
    readonly property int textSizeNav: 16
    readonly property int textSizeHeading: 17

    // --- Shape ---
    readonly property int radiusSmall: 4
    readonly property int radiusStd: 8
    readonly property int radiusLarge: 12

    // --- Motion (milliseconds) ---
    readonly property int durationFast: 100
    readonly property int durationStd: 150
    readonly property int durationTheme: 200

    // --- Layout ---
    readonly property int rowHeight: 36
    readonly property int headerBarHeight: 48
    readonly property int headerRowHeight: 32
    readonly property int leftMargin: 16

    // --- Lists ---
    readonly property color rowAlternateTint: Qt.rgba(1, 1, 1, 0.02)  // dark mode

    // --- ScrollBars ---
    readonly property color scrollBarResting: Qt.rgba(1, 1, 1, 0.4)
}
