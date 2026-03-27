import json
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def fill_diary_entries():
    # Load credentials
    try:
        with open('credentials.json', 'r') as f:
            creds = json.load(f)
    except FileNotFoundError:
        print("ERROR: credentials.json not found.")
        return

    # Load diary entries
    with open('project_diary_entries.json', 'r') as f:
        entries = json.load(f)

    print(f"Loaded {len(entries)} entries.")

    # Initialize WebDriver
    print("Initializing WebDriver...")
    try:
        driver = webdriver.Chrome()
    except:
        try:
             driver_path = ChromeDriverManager().install()
             service = Service(driver_path)
             driver = webdriver.Chrome(service=service)
        except Exception as e2:
             print(f"CRITICAL ERROR: {e2}")
             return

    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    def force_click(elem):
        driver.execute_script("arguments[0].click();", elem)

    def highlight(elem):
        driver.execute_script("arguments[0].style.border='3px solid red'", elem)

    try:
        # 1. Login Phase
        print("Navigating to login page...")
        driver.get("https://vtu.internyet.in/sign-in")
        
        print("Logging in...")
        try:
            # User provided XPaths
            email_xpath = "/html/body/div[1]/div/main/main/div/div[1]/div[2]/form/fieldset/div[1]/div/div/input"
            pass_xpath = "/html/body/div[1]/div/main/main/div/div[1]/div[2]/form/fieldset/div[2]/div/div/input"
            
            wait.until(EC.presence_of_element_located((By.XPATH, email_xpath))).send_keys(creds['email'])
            driver.find_element(By.XPATH, pass_xpath).send_keys(creds['password'])
            
            driver.find_element(By.XPATH, "//button[@type='submit'] | //button[contains(text(), 'Sign In')]").click()
            
            wait.until(EC.url_contains("dashboard"))
            print("Login successful.")
            time.sleep(2)
            
        except Exception as e:
            print(f"Login failed: {e}")
            input("Please log in manually and press Enter...")

        # 2. Process Entries
        diary_url = "https://vtu.internyet.in/dashboard/student/project-diary"


        for i, entry in enumerate(entries):
            print(f"Processing Week {entry['week']} ({entry['date']})...")
            
            if driver.current_url != diary_url:
                driver.get(diary_url)
                time.sleep(3)

            # Check for "Create" button
            try:
                create_btn = driver.find_elements(By.XPATH, "//button[contains(text(), 'Create') or contains(text(), 'Add Entry')]")
                if create_btn:
                    create_btn[0].click()
                    time.sleep(2)
            except: pass

            # --- Step 1: Project & Date ---
            
            # Select Project
            print("Selecting Project...")
            project_selected = False
            
            # Application 1: Try finding a hidden <select> (User suggestion)
            try:
                print("  Debug: Checking for hidden <select> element...")
                select_xpath = "/html/body/div[1]/div/main/div/div/main/div/div[2]/form/fieldset/div[2]/div/select"
                select_elem = driver.find_element(By.XPATH, select_xpath)
                
                # Make it visible if hidden (common hack)
                driver.execute_script("arguments[0].style.display = 'block';", select_elem)
                time.sleep(0.5)
                
                sel = Select(select_elem)
                sel.select_by_index(1) # Assuming index 1 is the project
                print("  Debug: Selected project via hidden <select>.")
                project_selected = True
                
            except Exception as sel_e:
                 print(f"  Debug: Hidden select approach failed: {sel_e}")

            # Application 2: Keyboard Navigation (Fallback)
            if not project_selected:
                try:
                    print("  Debug: Trying Keyboard Navigation (Down/Enter)...")
                    trigger_xpath = "/html/body/div[1]/div/main/div/div/main/div/div[2]/form/fieldset/div[2]/div/button"
                    trigger = wait.until(EC.element_to_be_clickable((By.XPATH, trigger_xpath)))
                    highlight(trigger)
                    
                    # Click to focus
                    force_click(trigger)
                    time.sleep(1)
                    
                    # Send Keys
                    actions = webdriver.ActionChains(driver)
                    actions.send_keys(Keys.DOWN).perform()
                    time.sleep(0.5)
                    actions.send_keys(Keys.ENTER).perform()
                    
                    print("  Debug: Sent DOWN + ENTER keys.")
                    project_selected = True
                    
                except Exception as key_e:
                    print(f"  Debug: Keyboard approach failed: {key_e}")
            
            # Validation
            print("Project selection attempt complete.")

            time.sleep(1)

            # Enter Date
            print(f"Entering Date: {entry['date']}...")
            try:
                # Parse Date: DD-MM-YYYY
                dt = datetime.datetime.strptime(entry['date'], "%d-%m-%Y")
                target_day = str(dt.day)
                target_month = dt.strftime("%b") # "Jan", "Feb"
                target_year = str(dt.year)
                
                # 1. Click Date Trigger
                date_btn_xpath = "/html/body/div[1]/div/main/div/div/main/div/div[2]/form/fieldset/div[3]/div/button"
                print(f"  Debug: Clicking Date Trigger: {date_btn_xpath}")
                date_btn = driver.find_element(By.XPATH, date_btn_xpath)
                highlight(date_btn)
                force_click(date_btn)
                time.sleep(1)
                
                # 2. Select Year
                year_xpath = "/html/body/div[3]/div/div/div/div/div/div/span[2]/select"
                print(f"  Debug: Selecting Year '{target_year}' via {year_xpath}")
                year_elem = wait.until(EC.presence_of_element_located((By.XPATH, year_xpath)))
                try:
                    Select(year_elem).select_by_visible_text(target_year)
                except Exception as e:
                    print(f"  > Standard year select failed: {e}. Trying send_keys.")
                    year_elem.send_keys(target_year)
                time.sleep(1) # Let React rerender the calendar table
                
                # 3. Select Month
                month_xpath = "/html/body/div[3]/div/div/div/div/div/div/span[1]/select"
                print(f"  Debug: Selecting Month '{target_month}' via {month_xpath}")
                month_elem = wait.until(EC.presence_of_element_located((By.XPATH, month_xpath)))
                sel_m = Select(month_elem)
                try:
                    sel_m.select_by_visible_text(target_month)
                except Exception as e:
                    print(f"  > Standard month select failed: {e}. Trying send_keys.")
                    month_elem.send_keys(target_month)
                
                time.sleep(1) # CRITICAL: Wait for React to render the NEW month's days before clicking!
                
                # Check Month
                curr_month = sel_m.first_selected_option.text
                if target_month.lower() not in curr_month.lower():
                     print(f"  > WARNING: Month might be wrong! Expected: {target_month}, Found: {curr_month}")

                # 4. Click Day (Dynamic)
                print(f"  Debug: Picking day: {target_day}")
                day_xpath = f"/html/body/div[3]/div/div/div/div/table/tbody//button[normalize-space(text())='{target_day}']"
                days = driver.find_elements(By.XPATH, day_xpath)
                
                clicked_day = False
                for d in days:
                    if d.is_displayed():
                        cls = d.get_attribute("class") or ""
                        try:
                            parent_cls = d.find_element(By.XPATH, "..").get_attribute("class") or ""
                        except:
                            parent_cls = ""
                        aria_hidden = d.get_attribute("aria-hidden") or "false"
                        disabled = d.get_attribute("disabled")
                        
                        # Radix UI / Shadcn often put 'outside' on the parent <td> or the button itself
                        if "outside" not in cls.lower() and "outside" not in parent_cls.lower() and aria_hidden != "true" and not disabled:
                            force_click(d)
                            clicked_day = True
                            print(f"    > Clicked primary day button: {target_day}")
                            break
                
                # Fallback if primary not found
                if not clicked_day and days:
                    for d in days:
                        if d.is_displayed():
                            force_click(d)
                            clicked_day = True
                            print(f"    > Clicked fallback day button: {target_day}")
                            break
                            
                if not clicked_day:
                     print("  > WARNING: Could not find clickable day button.")
                     
                time.sleep(1.5)
                
                # 5. VERIFICATION
                print("  Debug: Verifying selected date...")
                date_btn_check = driver.find_element(By.XPATH, date_btn_xpath)
                btn_text = date_btn_check.text.lower()
                
                if target_year in btn_text and target_day in btn_text and target_month.lower() in btn_text:
                    print(f"  > Date Verified Successfully: {date_btn_check.text}")
                elif entry['date'] in btn_text or dt.strftime("%Y-%m-%d") in btn_text or dt.strftime("%m/%d/%Y") in btn_text:
                    print(f"  > Date Verified Successfully (Numeric): {date_btn_check.text}")
                else:
                    if "pick a date" not in btn_text:
                        print(f"  > CRITICAL ERROR: Date Verification Failed! Button text: '{date_btn_check.text}', Expected parts: {target_day}, {target_month}, {target_year}")
                        raise Exception(f"Date Verification Failed for Week {entry['week']}")
                    else:
                        print("  > CRITICAL ERROR: Date not picked ('Pick a Date' still present).")
                        raise Exception(f"Date Verification Failed for Week {entry['week']}")

            except Exception as e:
                print(f"  > Date error: {e}")
                print("  > HALTING AUTOMATION DUE TO CRITICAL DATE ERROR.")
                return # STOP AUTOMATION completely

            time.sleep(1)

            # Click Continue
            print("Clicking Continue...")
            try:
                continue_xpath = "/html/body/div[1]/div/main/div/div/main/div/div[2]/form/fieldset/div[4]/button"
                continue_btn = driver.find_element(By.XPATH, continue_xpath)
                highlight(continue_btn)
                force_click(continue_btn)
                print("Clicked Continue.")
            except Exception as e:
                print(f"  > Continue error: {e}")
        
            time.sleep(3) # Wait for animation
            
            # --- Step 2: Details ---
            print("In Details Section...")
            
            # Work Summary
            print("Filling Work Summary...")
            try:
                # Try finding by name or just first textarea
                summary_box = wait.until(EC.presence_of_element_located((By.NAME, "work_summary")))
                summary_box.clear()
                summary_box.send_keys(entry['work_summary'])
            except:
                try:
                    # Fallback to generic textarea
                    txts = driver.find_elements(By.TAG_NAME, "textarea")
                    if txts:
                        txts[0].clear()
                        txts[0].send_keys(entry['work_summary'])
                except Exception as e:
                    print(f"  > Work Summary error: {e}")

            time.sleep(1)

            # Hours Worked
            print("Filling Hours...")
            try:
                hours_input = driver.find_element(By.NAME, "hours_worked")
                hours_input.clear()
                hours_input.send_keys(str(entry['hours_worked']))
            except:
                 try:
                    # Try finding by label if possible, or generic input type number
                    # hours_input = driver.find_element(By.XPATH, "//label[contains(., 'Hours')]/following::input[1]")
                    hours_input = driver.find_element(By.XPATH, "//input[@type='number']")
                    hours_input.clear()
                    hours_input.send_keys(str(entry['hours_worked']))
                 except Exception as e:
                    print(f"  > Hours error: {e}")

            time.sleep(1)

            # Learnings / Outcomes
            print("Filling Learnings...")
            try:
                # User provided XPath for Learnings
                learnings_xpath = "/html/body/div[1]/div/main/div/div/main/div/div[3]/form/fieldset/div[7]/div/div[1]/div[2]/textarea"
                learnings_box = driver.find_element(By.XPATH, learnings_xpath)

                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", learnings_box)
                time.sleep(0.5)

                learnings_box.clear()
                learnings_box.send_keys(entry['learnings_outcomes'])
            except Exception as e:
                print(f"  > Learnings error: {e}")

            time.sleep(1)

            # Skills Used
            print("Selecting Skills...")
            try:
                skills_xpath = "/html/body/div[1]/div/main/div/div/main/div/div[3]/form/fieldset/div[10]/div/div/div[1]/div[1]/div[2]"
                print(f"  Debug: Finding skills element: {skills_xpath}")
                
                skills_elem = wait.until(EC.element_to_be_clickable((By.XPATH, skills_xpath)))
                
                # Ensure element is in view
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", skills_elem)
                time.sleep(1)
                
                # Click to focus - Standard click is better for focus than JS click
                try:
                    skills_elem.click()
                    print("  Debug: Clicked skills element (Standard).")
                except Exception as click_err:
                    print(f"  Debug: Standard click failed ({click_err}), trying Force Click...")
                    force_click(skills_elem)
                
                time.sleep(1)
                
                # Initialize ActionChains
                actions = webdriver.ActionChains(driver)
                
                # Just in case, try clicking with ActionChains too
                actions.move_to_element(skills_elem).click().perform()
                
                for skill in entry['skills_used']:
                    print(f"  - Adding skill: {skill}")
                    # Type skill and press Enter
                    actions.send_keys(skill).perform()
                    time.sleep(1.5) # Wait for suggestions
                    actions.send_keys(Keys.ENTER).perform()
                    time.sleep(0.5)
                
                # Close dropdown / Unfocus
                try:
                    driver.find_element(By.TAG_NAME, "h1").click()
                except: pass
            
            except Exception as e:
                print(f"  > Skills error: {e}")
                
            # Save
            # Save
            print("Saving...")
            try:
                save_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Save') or contains(text(), 'Submit')]")
                # Scroll to it just in case
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)
                time.sleep(0.5)
                force_click(save_btn)
                print("Entry saved.")
                time.sleep(5) # Wait for network/redirect
            except Exception as e:
                print(f"Error clicking Save: {e}")
            
            print(f"Week {entry['week']} completed.")

    except Exception as e:
        print(f"Global Error: {e}")
    
    finally:
        print("Done.")
        # Keep browser open per user request
        if 'driver' in locals():
            input("Processing complete. Press Enter to close browser...")
            try:
                driver.quit()
            except: pass

if __name__ == "__main__":
    fill_diary_entries()
