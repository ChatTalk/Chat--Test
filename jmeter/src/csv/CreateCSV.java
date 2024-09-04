package csv;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

public class CreateCSV {
    public static void main(String[] args) {
        String csvFile = "users.csv";
        int start = 2; // 시작 번호
        int end = 999; // 끝 번호
        String password = "test";

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(csvFile))) {
            // CSV 헤더 작성
            writer.write("email,password");
            writer.newLine();

            // CSV 데이터 작성
            for (int n = start; n <= end; n++) {
                String email = "test" + n + "@test.com";
                writer.write(email + "," + password);
                writer.newLine();
            }

            System.out.println("CSV 파일 생성 완료: " + csvFile);

        } catch (IOException e) {
            System.err.println(e.getMessage());
        }
    }
}
