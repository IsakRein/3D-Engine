public class Player {
    String name;
    String country;
    int score;

    public Player(String name, String country, int score) {
        this.name = name;
        this.country = country;
        this.score = score;
    }

    public String toString() {
        return "Player " + name + " from " + country + " scored " + score + " points";
    }
}
