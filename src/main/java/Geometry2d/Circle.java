package Geometry2d;

import java.util.HashMap;
import java.util.Map;

public class Circle implements Figure {
    private final Double radius;

    public Circle(Double R) {
        radius = R;
    }

    public Double area() {
        return Math.PI * Math.pow(radius, 2);
    }

    public Double perimeter() {
        return 2 * Math.PI * radius;
    }

    public String ToString() {
        Map<String, Double> stringCircle = new HashMap<>();
        stringCircle.put("Radius", radius);
        stringCircle.put("Area", area());
        stringCircle.put("Perimeter", perimeter());

        return stringCircle.toString();
    }
}
