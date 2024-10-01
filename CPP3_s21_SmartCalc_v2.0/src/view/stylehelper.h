#ifndef STYLEHELPER_H
#define STYLEHELPER_H

#include <QString>

class StyleHelper {
 public:
  static QString getInputDisplayLabelStyle();
  static QString getLeftWidgetButtonsStyle();
  static QString getRightWidgetButtonsStyle();
  static QString getMainBackground();
  static QString getSizeNonActiveButtonStyle();
  static QString getSizeActiveButtonStyle();

  static QString getGraphLabelXYStyle();
  static QString getGraphLabelXYNumberStyle();
  static QString getWidgetDrawSpeedStyle();

  static QString getAnimationTurnButtonStyle();
  static QString getAnimationOffButtonStyle();
  static QString getAnimationTurnActiveButtonStyle();
  static QString getAnimationOffActiveButtonStyle();
};

#endif  // STYLEHELPER_H
