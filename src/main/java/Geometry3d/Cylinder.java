package Geometry3d;

import Geometry2d.Circle;

public class Cylinder {
    private Circle bottom;
    private Double height;

    public Cylinder(Double R, Double H) {
        try {

            bottom = new Circle(R);
            height = H;
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public Double Volume() {
        return bottom.area() * height;
    }
}
