#ifndef CCDCONTROLLER_H
#define CCDCONTROLLER_H

#include <QMainWindow>

namespace Ui {
class ccdcontroller;
}

class ccdcontroller : public QMainWindow
{
    Q_OBJECT

public:
    explicit ccdcontroller(QWidget *parent = 0);
    ~ccdcontroller();

private:
    Ui::ccdcontroller *ui;
};

#endif // CCDCONTROLLER_H
