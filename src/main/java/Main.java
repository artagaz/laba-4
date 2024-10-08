import Exeptions.*;
import Geometry2d.Circle;
import Geometry2d.Rectangle;
import Geometry3d.*;

public class Main {
    public static void main(String[] args) {

        Circle circle;
        Cylinder cylinder;
        Rectangle rectangle;
        try {
            rectangle = new Rectangle(10.0, 10.0);
            circle = new Circle(10.0);
            cylinder = new Cylinder(10.0, 10.0);
        } catch (NegativeSideException | NegativeRadiusExeption e) {
            throw new RuntimeException(e);
        }

        System.out.println("rectangle:" + rectangle.ToString());
        System.out.println("circle:" + circle.ToString());
        System.out.println("cylinder:" + cylinder.Volume());

        //Exeptions
//        try {
//            Rectangle rectangle = new Rectangle(-10.0, 10.0);
//        } catch (NegativeSideException e) {
//            throw new RuntimeException(e);
//        }
//        try {
//            Circle circle = new Circle(-10.0);
//        } catch (NegativeRadiusExeption e) {
//            throw new RuntimeException(e);
//        }
//        try {
//            Cylinder cylinder = new Cylinder(-10.0, 10.0);
//        } catch (NegativeSideException e) {
//            throw new RuntimeException(e);
//        }

    }
}
