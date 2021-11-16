package com.easin.serverTest.entities ;

import javax.persistence.*;
import javax.validation.constraints.*;
import lombok.*;
import lombok.extern.slf4j.Slf4j;
import io.swagger.annotations.ApiModelProperty;
import io.swagger.annotations.ApiModel;
import org.hibernate.annotations.GenericGenerator;
import java.util.Date;




/**
 * Class representing the Address parameters
 */
@ApiModel(description = "Class representing the Address parameters")
@Slf4j
@Getter
@Setter
@AllArgsConstructor
@ToString
@Entity
public class Address extends BaseEntity {

    @Id
    @GeneratedValue(generator = "system-uuid", strategy = GenerationType.IDENTITY)
    @GenericGenerator(name = "system-uuid", strategy = "uuid2")
    @ApiModelProperty(hidden = true)
    protected String Id;
    /** address of the Company */
    @ApiModelProperty(value = " address of the Company ")
    @Column(nullable = false)
    private String address;

    /** contry of the Company */
    @ApiModelProperty(value = " contry of the Company ")
    @Column(nullable = false)
    private String contry;

    /** town of the Company */
    @ApiModelProperty(value = " town of the Company ")
    @Column(nullable = false)
    private String town;

    /** zipcode of the Company */
    @ApiModelProperty(value = " zipcode of the Company ")
    @Column(nullable = false)
    private Integer zipcode;

    /**
    * default constructor
    */
    public Address() {
        super();
    }
}
