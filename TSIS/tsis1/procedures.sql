-- add_phone
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE v_id INT;
BEGIN
    SELECT id INTO v_id FROM contacts WHERE name = p_contact_name;
    IF v_id IS NOT NULL THEN
        INSERT INTO phones(contact_id, phone, type)
        VALUES(v_id, p_phone, p_type);
    END IF;
END;
$$;

-- move_to_group
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE v_gid INT;
BEGIN
    SELECT id INTO v_gid FROM groups WHERE name = p_group_name;
    IF v_gid IS NULL THEN
        INSERT INTO groups(name) VALUES(p_group_name) RETURNING id INTO v_gid;
    END IF;
    UPDATE contacts SET group_id = v_gid WHERE name = p_contact_name;
END;
$$;

-- search_contacts (расширенная версия из practice 8)
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(name VARCHAR, email VARCHAR, phone VARCHAR, type VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT c.name, c.email, p.phone, p.type
    FROM contacts c
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE c.name  ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%';
END;
$$;