package Geometry2d;

import Exeptions.NegativeSideException;

import java.util.HashMap;
import java.util.Map;

public class Rectangle {
    private final Double a;
    private final Double b;

    public Rectangle(Double A, Double B) throws NegativeSideException {
        if (A <= 0) throw new NegativeSideException("A<=0");
        if (B <= 0) throw new NegativeSideException("B<=0");
        else {a = A; b = B;}
    }

    public Double area() {
        return a * b;
    }

    public Double perimeter() {
        return a * 2 + b * 2;
    }

    public String ToString() {
        Map<String, Double> stringRectangle = new HashMap<>();
        stringRectangle.put("A", a);
        stringRectangle.put("B", a);
        stringRectangle.put("Area", area());
        stringRectangle.put("Perimeter", perimeter());

        return stringRectangle.toString();
    }
}
