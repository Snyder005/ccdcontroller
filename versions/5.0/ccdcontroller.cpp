#include "ccdcontroller.h"
#include "ui_ccdcontroller.h"

ccdcontroller::ccdcontroller(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::ccdcontroller)
{
    ui->setupUi(this);
}

ccdcontroller::~ccdcontroller()
{
    delete ui;
}
