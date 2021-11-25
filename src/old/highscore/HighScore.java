import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class HighScore {

    public static void printHighScores(String filename) {
        BufferedReader inputStream = null;

        try {
            inputStream = new BufferedReader(new FileReader(filename));
            String line;
            String[] playerData;
            while ((line = inputStream.readLine()) != null) {
                playerData = line.split(",");
                System.out.println("Player " + playerData[0] + " scored " + playerData[1] + " points");
            }
        } catch (IOException ioe) {
            System.out.println(ioe.getMessage());
        }
    }

    public static void main(String[] args) {
        printHighScores("scores.txt");
    }
}
