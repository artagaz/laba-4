package Geometry3d;

import Exeptions.NegativeRadiusExeption;
import Exeptions.NegativeSideException;
import Geometry2d.Circle;

public class Cylinder {
    private Circle bottom;
    private Double height;

    public Cylinder(Double R, Double H) throws NegativeSideException {
        if (H<=0) throw new NegativeSideException("Height <= 0");
        else height = H;

        try {
            bottom = new Circle(R);
        } catch (NegativeRadiusExeption e) {
            throw new RuntimeException(e);
        }
    }

    public Double Volume() {
        return bottom.area() * height;
    }
}
