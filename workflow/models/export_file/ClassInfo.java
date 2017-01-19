import java.lang.annotation.*;

/**
 * Created by root on 1/6/17.
 */

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@Documented
public @interface ClassInfo {

    int algorithm_category() default 0;

    boolean is_visualization() default false;

    int[] visualization_category() default -1;
}

