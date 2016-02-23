#include "ccdcontroller.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    ccdcontroller w;
    w.show();

    return a.exec();
}
