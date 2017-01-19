/**
 * Created by root on 1/6/17.
 */
import java.lang.annotation.*;

@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.TYPE})
@Documented
public @interface FieldInfo {

    String parameter_category() default "parameters"; //inputs, outputs, parameters

    String name() default "";

    String type() default ""; //text, selection, filelist, database

    String[] choices() default ""; // selection

    String belong_to() default ""; //algorithm_category = 1

    int stage() default 0; //algorithm_category = 1

    String description() default "";

}
