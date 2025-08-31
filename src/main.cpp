#include "main.h"
#include "pros/apix.h"      // LVGL v5.3 + PROS shims (must be before team_logo.h)
#include "pros/misc.h"
#include "team_logo.h"      // declares lv_img_dsc_t team_logo


static void show_splash() {
	lv_obj_t* img = lv_img_create(lv_scr_act(), NULL);
	lv_img_set_src(img, &team_logo);
	lv_obj_align(img, NULL, LV_ALIGN_CENTER, 0, 0);
	pros::delay(2000);
	lv_obj_del(img);
}

/**
 * Runs initialization code. This occurs as soon as the program is started.
 *
 * All other competition modes are blocked by initialize; it is recommended
 * to keep execution time for this mode under a few seconds.
 */
void initialize() {
	show_splash();
}

/**
 * Runs while the robot is in the disabled state of Field Management System or
 * the VEX Competition Switch, following either autonomous or opcontrol. When
 * the robot is enabled, this task will exit.
 */
void disabled() {}

/**
 * Runs after initialize(), and before autonomous when connected to the Field
 * Management System or the VEX Competition Switch. This is intended for
 * competition-specific initialization routines, such as an autonomous selector
 * on the LCD.
 *
 * This task will exit when the robot is enabled and autonomous or opcontrol
 * starts.
 */
void competition_initialize() {}

/**
 * Runs the user autonomous code. This function will be started in its own task
 * with the default priority and stack size whenever the robot is enabled via
 * the Field Management System or the VEX Competition Switch in the autonomous
 * mode. Alternatively, this function may be called in initialize or opcontrol
 * for non-competition testing purposes.
 *
 * If the robot is disabled or communications is lost, the autonomous task
 * will be stopped. Re-enabling the robot will restart the task, not re-start it
 * from where it left off.
 */
void autonomous() {
	// Autonomous code here
}

/**
 * Runs the operator control code. This function will be started in its own task
 * with the default priority and stack size whenever the robot is enabled via
 * the Field Management System or the VEX Competition Switch in the operator
 * control mode.
 *
 * If no competition control is connected, this function will run immediately
 * following initialize().
 *
 * If the robot is disabled or communications is lost, the
 * operator control task will be stopped. Re-enabling the robot will restart the
 * task, not resume it from where it left off.
 */
void opcontrol() {
	// Basic motor control
	pros::Controller master(pros::E_CONTROLLER_MASTER);
	pros::Motor left_mtr(1, pros::v5::MotorGears::green, pros::v5::MotorUnits::degrees);
	pros::Motor right_mtr(2, pros::v5::MotorGears::green, pros::v5::MotorUnits::degrees);
	right_mtr.set_reversed(true);   // reverse direction

	while (true) {
		int left = master.get_analog(pros::E_CONTROLLER_ANALOG_LEFT_Y);
		int right = master.get_analog(pros::E_CONTROLLER_ANALOG_RIGHT_Y);

		left_mtr.move(left);
		right_mtr.move(right);

		pros::delay(20);
	}
}