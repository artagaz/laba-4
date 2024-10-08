package Exeptions;

public class NegativeRadiusExeption extends Exception {
    public NegativeRadiusExeption()
    {
        super("R<=0");
    }
}
